from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from json import loads as from_json
from multiprocessing import Process, set_start_method
from random import choices, randint, choice
import string
from tempfile import NamedTemporaryFile
from time import sleep
from typing import Optional, Dict, List, Any, Tuple, Callable

import docker
from funcy import first

from robotnikmq.config import ServerConfig, server_config

USERNAME = "robotnik"
PASSWORD = "hackme"
VIRTUAL_HOST = "/robotnik"

META_QUEUE = "skynet.legion"

@contextmanager
def sub_process(
        target: Callable,
        args: Optional[Tuple[Any, ...]] = None,
        name: Optional[str] = None,
        terminate: bool = True,
):
    proc = Process(target=target, args=args or (), name=name)
    proc.start()
    try:
        sleep(0.2)
        yield proc
    finally:
        if terminate:
            proc.terminate()
        proc.join()


def random_string(length: int,
                  lower_case: bool = True,
                  upper_case: bool = True,
                  digits: bool = True,
                  punctuation: bool = False) -> str:
    alphabet = []
    if lower_case:
        alphabet += string.ascii_lowercase
    if upper_case:
        alphabet += string.ascii_uppercase
    if digits:
        alphabet += string.digits
    if punctuation:
        alphabet += string.punctuation
    return ''.join(choices(alphabet, k=length))


def random_upper_case_only_string(length: int) -> str:
    return random_string(length, lower_case=False, upper_case=True, digits=False, punctuation=False)


@dataclass(frozen=True)
class RabbitMQContainerConnInfo:
    name: str
    http_port: int
    amqp_port: int
    username: str
    password: str

    def server_config(self) -> ServerConfig:
        return server_config(host='localhost',
                             port=self.amqp_port,
                             user=self.username,
                             password=self.password,
                             vhost='/')


class RabbitMQContainer:
    image_name = "rabbitmq:3-management"
    internal_amqp_port = 5672
    internal_http_port = 15672

    @staticmethod
    def _temp_file(contents: bytes):
        _file = NamedTemporaryFile()
        _file.write(contents)
        _file.seek(0)
        return _file

    def __init__(self,
                 name: Optional[str] = None,
                 amqp_port: Optional[int] = None,
                 http_port: Optional[int] = None,
                 username: str = "rabbit",
                 password: Optional[str] = None,
                 erlang_cookie: Optional[str] = None,
                 configuration: Optional[str] = None,
                 extra_hosts: Optional[Dict] = None):
        self.name = name or f'rabbitmq-{random_string(8)}'
        self.amqp_port = amqp_port or randint(20_000, 65_000)
        self.http_port = http_port or randint(20_000, 65_000)
        self.default_username = username
        self.default_password = password or random_string(20)
        self.extra_hosts = extra_hosts or {}
        self.erlang_cookie = erlang_cookie or random_upper_case_only_string(32)
        self.erlang_cookie_file = self._temp_file(self.erlang_cookie.encode())
        self.configuration = configuration
        self.configuration_file = self._temp_file(configuration.encode()) if self.configuration is not None else None
        self.env = {'RABBITMQ_NODENAME': f"rabbit@{self.name}",
                    'RABBITMQ_DEFAULT_USER': self.default_username,
                    'RABBITMQ_DEFAULT_PASS': self.default_password}
        client = docker.from_env()
        self.container = client.containers.create(self.image_name, name=self.name,
                                                  detach=True,
                                                  auto_remove=True,
                                                  environment=self.env,
                                                  hostname=self.name,
                                                  ports={self.internal_amqp_port: self.amqp_port,
                                                         self.internal_http_port: self.http_port},
                                                  volumes=self._volumes,
                                                  extra_hosts=self.extra_hosts)

    @property
    def conn_info(self) -> RabbitMQContainerConnInfo:
        return RabbitMQContainerConnInfo(name=self.name,
                                         amqp_port=self.amqp_port,
                                         http_port=self.http_port,
                                         username=self.default_username,
                                         password=self.default_password)

    @property
    def _volumes(self) -> Dict:
        if self.configuration is None:
            return {self.erlang_cookie_file.name:
                        {'bind': '/var/lib/rabbitmq/.erlang.cookie',
                         'mode': 'rw'}}
        else:
            return {self.erlang_cookie_file.name:
                        {'bind': '/var/lib/rabbitmq/.erlang.cookie',
                         'mode': 'rw'},
                    self.configuration_file.name:
                        {'bind': '/etc/rabbitmq/rabbitmq.conf',
                         'mode': 'rw'}}

    def start(self) -> None:
        self.container.start()
        print(f"""RabbitMQ Container {self.name} Started
   Management UI at: http://localhost:{self.http_port}
     Username: {self.default_username}
     Password: {self.default_password}
   AMQP at: http://localhost:{self.amqp_port}
     Username: {self.default_username}
     Password: {self.default_password}""")

    def stop(self) -> None:
        try:
            print(f"Stopping RabbitMQ Container {self.name}...")
            self.container.stop()
        finally:
            self.erlang_cookie_file.close()
            print(f"RabbitMQ Container {self.name} stopped.")

    def kill(self) -> None:
        self.container.kill()

    def logs(self):
        yield from self.container.logs(stream=True)

    def exec_run(self, *args, **kwargs):
        return self.container.exec_run(*args, **kwargs)

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.stop()


class RabbitMQCluster:
    MAX_NODES = 64
    SUBNET = "192.168.57.0/24"
    GATEWAY = "192.168.57.1"

    def __init__(self, name: str, num_nodes: int = 3):
        self.name = name
        if num_nodes < 1:
            raise ValueError(
                f"The requested number of nodes ({num_nodes}) is less than 1, can't make a cluster from that...")
        if num_nodes > self.MAX_NODES:
            raise ValueError(
                f"The requested number of nodes {num_nodes} is greater than the maximum allowed: {self.MAX_NODES}")
        self.num_nodes = num_nodes
        self.erlang_cookie = random_upper_case_only_string(32)
        self.default_password = random_string(20)
        self.client = docker.from_env()
        self.executor = ThreadPoolExecutor(max_workers=self.num_nodes)
        self.client.networks.prune()
        self.network = self.client.networks.create(name=f"{self.name}-net",
                                                   driver="bridge",
                                                   ipam=docker.types.IPAMConfig(
                                                       pool_configs=[docker.types.IPAMPool(
                                                           subnet=self.SUBNET,
                                                           gateway=self.GATEWAY)
                                                       ]))
        self.nodes = [self._create_node(i) for i in range(self.num_nodes)]

    def _create_node(self, identifier: int) -> RabbitMQContainer:
        rmq_node: RabbitMQContainer = RabbitMQContainer(name=self._node_name(identifier),
                                                        erlang_cookie=self.erlang_cookie,
                                                        configuration=self._cluster_config,
                                                        password=self.default_password,
                                                        extra_hosts=self._hosts)
        self.network.connect(rmq_node.container, ipv4_address=self._ip_addr(identifier))
        return rmq_node

    @staticmethod
    def _ip_addr(identifier: int) -> str:
        return f"192.168.57.{10 + identifier}"

    def _node_name(self, identifier: int) -> str:
        return f"{self.name}-node{identifier}"

    @property
    def _cluster_config(self) -> str:
        result = ["cluster_formation.peer_discovery_backend = rabbit_peer_discovery_classic_config",
                  "cluster_partition_handling = autoheal"]
        for i in range(self.num_nodes):
            result.append(f"cluster_formation.classic_config.nodes.{i} = rabbit@{self._node_name(i)}")
        return '\n'.join(result)

    @property
    def _hosts(self) -> Dict[str, str]:
        return {self._node_name(i): self._ip_addr(i) for i in range(self.num_nodes)}

    @staticmethod
    def _stop(rmq_node: RabbitMQContainer) -> None:
        rmq_node.stop()

    @staticmethod
    def _start(rmq_node: RabbitMQContainer) -> None:
        rmq_node.start()

    def kill(self, conn_info: RabbitMQContainerConnInfo) -> None:
        first(n for n in self.nodes if n.name == conn_info.name).kill()

    def pause(self, conn_info: RabbitMQContainerConnInfo) -> None:
        first(n for n in self.nodes if n.name == conn_info.name).pause()

    def unpause(self, conn_info: RabbitMQContainerConnInfo) -> None:
        first(n for n in self.nodes if n.name == conn_info.name).unpause()

    @property
    def conn_info(self) -> List[RabbitMQContainerConnInfo]:
        return [rmq_node.conn_info for rmq_node in self.nodes]

    def _poll_until_clustering_successful(self) -> None:
        while 42:
            print("Waiting for cluster formation...")
            status = self.cluster_status()
            if status is not None and len(status['running_nodes']) == self.num_nodes:
                return
            sleep(0.5)

    def cluster_status(self) -> Optional[Dict]:
        exit_code, output = first(node for node in self.nodes).exec_run("rabbitmqctl cluster_status --formatter json")
        if exit_code == 0:
            return from_json(output.decode().strip())
        return None

    def _start_all(self) -> None:
        futures = [self.executor.submit(self._start, rmq_node) for rmq_node in self.nodes]
        for future in futures:
            try:
                future.result()
            except Exception as exc:
                print(exc)

    def clean_up(self):
        futures = [self.executor.submit(self._stop, rmq_node) for rmq_node in self.nodes]
        for future in futures:
            try:
                future.result()
            except Exception as exc:
                print(exc)
        self.client.networks.prune()

    def __enter__(self) -> 'RabbitMQCluster':
        self._start_all()
        self._poll_until_clustering_successful()
        return self

    def __exit__(self, *_):
        self.clean_up()

# with RabbitMQCluster('test-cluster', num_nodes=5) as cluster:
#     nodes = cluster.conn_info
#     sleep(10)
#     while 42:
#         sleep(10)
#         node = choice(nodes[1:])
#         delay = randint(20, 300)
#         print(f"Pausing {node.name} for {delay} seconds...")
#         cluster.pause(node)
#         sleep(delay)
#         print(f"Unpausing {node.name}...")
#         cluster.unpause(node)
