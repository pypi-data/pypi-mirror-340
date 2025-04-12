import json
from threading import Thread, Event
from pprint import pprint
from time import sleep

from pytest import raises, mark

import robotnikmq
from robotnikmq.config import server_config, RobotnikConfig
from robotnikmq.core import Message
from robotnikmq.error import UnableToConnect, MalformedMessage
from robotnikmq.log import log
from robotnikmq.subscriber import Subscriber
from robotnikmq.topic import Topic

from tests.integration.utils import META_QUEUE, RabbitMQCluster


try:
    from pytest_cov.embed import cleanup_on_sigterm  # type: ignore
except ImportError:
    pass
else:
    cleanup_on_sigterm()


def test_basic_broadcast(robotnikmq_config):
    topic = Topic(META_QUEUE, robotnikmq_config)
    topic.broadcast(Message.of({"stuff": "Hello world!"}))


@mark.slow
def test_unable_to_connect():
    config = RobotnikConfig(
        tiers=[
            [
                server_config("127.0.0.1", 1, "", "", ""),
                server_config("127.0.0.2", 1, "1", "1", "1"),
            ]
        ],
    )
    with raises(UnableToConnect) as exc:
        medium = Topic(META_QUEUE, config)
        medium.broadcast(Message.of({"stuff": "Hello world!"}))
    log.debug(str(exc))
    log.debug(str(exc.value))


def test_basic_broadcast_receive(robotnikmq_config):
    msg_received = Event()

    def sub():
        for msg in (
            Subscriber(config=robotnikmq_config).bind(exchange=META_QUEUE).consume()
        ):
            pprint(msg.to_dict())
            msg_received.set()
            break

    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "Hello world!"}))

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc = Thread(target=pub)
    pub_proc.start()
    assert msg_received.wait(timeout=5)
    pub_proc.join()
    sub_proc.join()


def test_subscriber_jitter(robotnikmq_config):
    subscriber = Subscriber(config=robotnikmq_config).bind(exchange=META_QUEUE)
    for _ in range(1000):
        assert 5.0 <= subscriber._jitter(10, 5) <= 15  # pylint: disable=W0212


def test_backoff_with_jitter(monkeypatch, robotnikmq_config):
    with monkeypatch.context() as mock:
        mock.setattr(robotnikmq.subscriber, 'sleep', lambda x: log.debug('sleep({})', x))
        sub = Subscriber(config=robotnikmq_config).bind(exchange=META_QUEUE)
        for _ in range(1000):
            assert (10 + sub.TIMEOUT_STEP - sub.TIMEOUT_JITTER) <= \
                   sub._backoff_with_jitter(10) \
                   <= (10 + sub.TIMEOUT_STEP + sub.TIMEOUT_JITTER)  # pylint: disable=W0212


def test_broadcast_malformed_message(robotnikmq_config):
    def sub():
        for msg in (
            Subscriber(config=robotnikmq_config)
            .bind(exchange=META_QUEUE)
            .consume(inactivity_timeout=2)
        ):
            assert msg is None
            break

    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.channel.basic_publish(
            exchange=META_QUEUE,
            routing_key="",
            body=json.dumps({"stuff": "Hello world!"}),
        )

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc = Thread(target=pub)
    pub_proc.start()
    pub_proc.join()
    sub_proc.join()


def test_subscriber_stop(robotnikmq_config):
    first_msg_received = Event()
    second_msg_received = Event()

    def sub():
        for msg in Subscriber(config=robotnikmq_config).bind(exchange=META_QUEUE).consume():
            pprint(msg.to_dict())
            if not first_msg_received.is_set():
                first_msg_received.set()
                break
            second_msg_received.set()

    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "first message"}))
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "second message"})
        )  # this message should not be received

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc = Thread(target=pub)
    pub_proc.start()
    assert first_msg_received.wait(timeout=1)
    assert not second_msg_received.wait(timeout=1)
    pub_proc.join()
    sub_proc.join()


def test_basic_broadcast_consume(robotnikmq_config):
    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "Hello world!"}))

    pub_proc = Thread(target=pub)
    pub_proc.start()
    stream = (
        Subscriber(config=robotnikmq_config)
        .bind(exchange=META_QUEUE)
        .consume(inactivity_timeout=0.1)
    )
    for msg in stream:
        if msg is not None:
            assert msg["stuff"] == "Hello world!"
            log.debug("Break")
            break
    pub_proc.join()


def test_consume_malformed_message(robotnikmq_config):
    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.channel.basic_publish(
            exchange=META_QUEUE, routing_key="", body=json.dumps({"stuff": "MALFORMED"})
        )
        medium.broadcast(Message.of({"stuff": "Hello world!"}))

    pub_proc = Thread(target=pub)
    pub_proc.start()
    for msg in (
        Subscriber(config=robotnikmq_config)
        .bind(exchange=META_QUEUE)
        .consume(inactivity_timeout=0.1)
    ):
        if msg is not None:
            assert msg["stuff"] == "Hello world!"
            break
    pub_proc.join()


def test_multiple_broadcast_single_receive(robotnikmq_config):
    msg_received = Event()

    def sub():
        for msg in (
            Subscriber(config=robotnikmq_config)
            .bind(exchange="stuff", binding_key="stuff.*")
            .consume()
        ):
            pprint(msg.to_dict())
            assert msg.contents["stuff"] != "Bad"
            assert msg.routing_key in {"stuff.something", "stuff.nothing"}
            msg_received.set()
            break

    def pub1():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (1)"}), routing_key="stuff.something"
        )

    def pub2():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (2)"}), routing_key="stuff.nothing"
        )

    def pub3():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "Bad"}), routing_key="bad.stuff.nothing")

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc1 = Thread(target=pub1)
    pub_proc1.start()
    pub_proc2 = Thread(target=pub2)
    pub_proc2.start()
    pub_proc3 = Thread(target=pub3)
    pub_proc3.start()
    assert msg_received.wait(timeout=5)
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    sub_proc.join()


def test_multiple_route_receive(robotnikmq_config):
    msg1_received = Event()
    msg2_received = Event()
    msg3_received = Event()

    def sub():
        for msg in (
            Subscriber(config=robotnikmq_config)
            .bind("stuff", "message.1")
            .bind("stuff", "message.2")
            .bind("stuff", "message.3")
            .consume()
        ):
            pprint(msg.to_dict())
            assert msg.contents["stuff"] != "Bad"
            if msg.route == "message.1":
                msg1_received.set()
            if msg.route == "message.2":
                msg2_received.set()
            if msg.route == "message.3":
                msg3_received.set()
            if msg1_received.is_set() and msg2_received.is_set() and msg3_received.is_set():
                break

    def pub1():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (1)"}), routing_key="message.1"
        )

    def pub2():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (2)"}), routing_key="message.2"
        )

    def pub3():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (3)"}), routing_key="message.3"
        )

    def pub_bad():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "Bad"}), routing_key="bad.stuff.nothing")

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc1 = Thread(target=pub1)
    pub_proc1.start()
    pub_proc2 = Thread(target=pub2)
    pub_proc2.start()
    pub_proc3 = Thread(target=pub3)
    pub_proc3.start()
    pub_proc_bad = Thread(target=pub_bad)
    pub_proc_bad.start()
    assert msg1_received.wait(timeout=5)
    assert msg2_received.wait(timeout=5)
    assert msg3_received.wait(timeout=5)
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    pub_proc_bad.join()
    sub_proc.join()


def test_multiple_queue_receive(robotnikmq_config):
    msg1_received = Event()
    msg2_received = Event()
    msg3_received = Event()

    def sub():
        for msg in (
            Subscriber(config=robotnikmq_config)
            .bind("stuff.1", "message.1")
            .bind("stuff.2", "message.2")
            .bind("stuff.3", "message.3")
            .consume()
        ):
            pprint(msg.to_dict())
            assert msg.contents["stuff"] != "Bad"
            if msg.route == "message.1":
                msg1_received.set()
            if msg.route == "message.2":
                msg2_received.set()
            if msg.route == "message.3":
                msg3_received.set()
            if msg1_received.is_set() and msg2_received.is_set() and msg3_received.is_set():
                break

    def pub1():
        medium = Topic(
            exchange="stuff.1",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (1)"}), routing_key="message.1"
        )

    def pub2():
        medium = Topic(
            exchange="stuff.2",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (2)"}), routing_key="message.2"
        )

    def pub3():
        medium = Topic(
            exchange="stuff.3",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (3)"}), routing_key="message.3"
        )

    def pub_bad():
        medium = Topic(
            exchange="stuff.1",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "Bad"}), routing_key="bad.stuff.nothing")

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc1 = Thread(target=pub1)
    pub_proc1.start()
    pub_proc2 = Thread(target=pub2)
    pub_proc2.start()
    pub_proc3 = Thread(target=pub3)
    pub_proc3.start()
    pub_proc_bad = Thread(target=pub_bad)
    pub_proc_bad.start()
    assert msg1_received.wait(timeout=5)
    assert msg2_received.wait(timeout=5)
    assert msg3_received.wait(timeout=5)
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    pub_proc_bad.join()
    sub_proc.join()


def test_multiple_broadcast_single_receive_msg_routing(robotnikmq_config):
    msg_received = Event()

    def sub():
        for msg in (
            Subscriber(config=robotnikmq_config)
            .bind(exchange="stuff", binding_key="stuff.*")
            .consume()
        ):
            pprint(msg.to_dict())
            assert msg.contents["stuff"] != "Bad"
            assert msg.routing_key in {"stuff.something", "stuff.nothing"}
            msg_received.set()
            break

    def pub1():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (1)"}, routing_key="stuff.something")
        )

    def pub2():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(
            Message.of({"stuff": "Hello world! (2)"}, routing_key="stuff.nothing")
        )

    def pub3():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
        )
        sleep(0.2)
        medium.broadcast(Message.of({"stuff": "Bad"}, routing_key="bad.stuff.nothing"))

    sub_proc = Thread(target=sub)
    sub_proc.start()
    pub_proc1 = Thread(target=pub1)
    pub_proc1.start()
    pub_proc2 = Thread(target=pub2)
    pub_proc2.start()
    pub_proc3 = Thread(target=pub3)
    pub_proc3.start()
    assert msg_received.wait(timeout=5)
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    sub_proc.join()


@mark.slow
def test_confirm_subscriber_reconnection_behavior_on_node_failure():
    """
    This test is designed to confirm that a subscriber will reconnect to another node in a cluster in accordance with
    its RobotnikMQ configuration tiers.
    """
    with RabbitMQCluster('test-cluster', num_nodes=2) as cluster:
        initial_msg_received = Event()
        first_node_shutdown = Event()
        msg_received_after_reconnect = Event()

        nodes = cluster.conn_info
        robotnik_config = RobotnikConfig.from_tiered([[nodes[0].server_config()], [nodes[1].server_config()]])

        def pub():
            """
            This function spams two different kinds of messages, one before the tier-1 node is shut down, and a
            different one after. Receiving both messages allows us to confirm that we have reconnected successfully
            and resumed receiving messages as expected.
            """
            medium = Topic(
                exchange="stuff",
                config=robotnik_config,
            )
            while 42:
                if msg_received_after_reconnect.is_set():
                    break
                sleep(0.2)
                if not first_node_shutdown.is_set():
                    if not msg_received_after_reconnect.is_set():
                        medium.broadcast(Message.of({"test": 1}, routing_key="before.node.shutdown"))
                else:
                    if not msg_received_after_reconnect.is_set():
                        medium.broadcast(Message.of({"test": 2}, routing_key="after.node.shutdown"))

        def sub():
            for msg in (Subscriber(config=robotnik_config)
                        .bind(exchange="stuff", binding_key="#.node.shutdown").consume()):
                if not first_node_shutdown.is_set():
                    assert msg['test'] == 1
                    print("First message received successfully, flagging...")
                    initial_msg_received.set()
                else:
                    assert initial_msg_received.is_set()
                    assert msg['test'] == 2
                    print("Post-node-shutdown message received successfully, flagging...")
                    msg_received_after_reconnect.set()
                    print("Subscriber thread shutting down successfully...")
                    break

        sub_thread = Thread(target=sub)
        pub_thread = Thread(target=pub)
        pub_thread.start()
        sub_thread.start()

        # wait until first message is received and then shutdown the tier-1 node
        assert initial_msg_received.wait(timeout=5)
        print("Killing tier-1 node...")
        cluster.kill(nodes[0])
        first_node_shutdown.set()
        print("Tier-1 node killed.")

        # wait for subscriber reconnect and assert that its receiving messages again
        assert msg_received_after_reconnect.wait(timeout=20)  # long timeout because it takes a while for the connection strategy to give up
