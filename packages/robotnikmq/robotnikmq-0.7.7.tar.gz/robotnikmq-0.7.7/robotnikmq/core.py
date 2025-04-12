import logging
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from json import loads as _from_json
from json.decoder import JSONDecodeError
from pathlib import Path
from random import sample
from threading import current_thread
from typing import Optional, Callable, Any, Dict, Union, Generator, List, TypedDict
from uuid import uuid4 as uuid, UUID

from arrow import Arrow, get as to_arrow, now
from funcy import first
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPError, AMQPConnectionError
from pydantic import BaseModel  # pylint: disable=E0611
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random, Retrying
from tenacity.after import after_log
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig, config_of, ServerConfig
from robotnikmq.error import UnableToConnect, MalformedMessage
from robotnikmq.log import log
from robotnikmq.utils import to_json as _to_json

AMQPErrorCallback = Optional[Callable[[AMQPError], None]]
ConnErrorCallback = Optional[Callable[[AMQPConnectionError], None]]


@contextmanager
def thread_name(name: Union[str, UUID]):
    thread = current_thread()
    original = thread.name
    thread.name = str(name)
    yield
    thread.name = original


@typechecked
def jsonable(content: Any) -> bool:
    try:
        _to_json(content)
        return True
    except (TypeError, OverflowError):
        return False


@typechecked
def valid_json(string: str) -> bool:
    try:
        _from_json(string)
        return True
    except JSONDecodeError:
        return False

@typechecked
class MessageTypedDict(TypedDict):
    contents: Dict[str, Any]
    routing_key: Optional[str]
    timestamp: Union[int, float]
    msg_id: str

@typechecked
@dataclass(frozen=True)
class Message:
    contents: Union[BaseModel, Dict[str, Any]]
    routing_key: str
    timestamp: Arrow
    msg_id: Union[str, UUID]

    @staticmethod
    def of(
        contents: Union[BaseModel, Dict],
        routing_key: Optional[str] = None,
        timestamp: Union[int, float, datetime, Arrow, None] = None,
        msg_id: Union[str, UUID, None] = None,
    ) -> 'Message':
        msg_id = msg_id or uuid()
        if not jsonable(contents):
            raise ValueError("Contents of message have to be JSON-serializeable")
        contents = contents.dict() if isinstance(contents, BaseModel) else contents
        routing_key: str = routing_key or ""
        timestamp: Arrow = to_arrow(timestamp) if timestamp is not None else now()
        return Message(contents, routing_key, timestamp, msg_id)

    def with_routing_key(self, routing_key: Optional[str]) -> 'Message':
        return Message.of(self.contents, routing_key, self.timestamp, self.msg_id)

    def to_dict(self) -> MessageTypedDict:
        return {
            "routing_key": self.routing_key,
            "contents": self.contents,
            "msg_id": str(self.msg_id),
            "timestamp": self.timestamp.int_timestamp,
        }

    def to_json(self) -> str:
        return _to_json(self.to_dict())

    @staticmethod
    def of_json(body: str) -> "Message":  # pylint: disable=C0103
        try:
            msg = _from_json(body)
            return Message.of(
                msg["contents"], msg["routing_key"], msg["timestamp"], msg["msg_id"]
            )
        except (JSONDecodeError, KeyError) as exc:
            raise MalformedMessage(body) from exc

    def __getitem__(self, key: str) -> Any:
        return self.contents[key]

    def keys(self):
        return self.contents.keys()

    def values(self):
        return self.contents.values()

    def __contains__(self, item: str) -> bool:
        return item in self.contents

    def __iter__(self):
        return iter(self.contents)

    @property
    def route(self) -> str:
        return self.routing_key


class Robotnik:
    # TODO: Add a connection-strategy object parameter that takes a configuration and when asked returns the next server
    #       to connect to because right now we just have pretty arbitrary retry parameters which may be appropriate in
    #       some cases, but not others. For example, subscribers should attempt to reconnect indefinitely, whereas
    #       publishers should not.
    @typechecked
    def __init__(
        self,
        config: Optional[RobotnikConfig] = None,
        config_paths: Optional[List[Path]] = None,
    ):
        config_paths = config_paths or [
            Path.cwd() / "robotnikmq.yaml",
            Path.home() / ".config" / "robotnikmq" / "robotnikmq.yaml",
            Path("/etc/robotnikmq/robotnikmq.yaml"),
            Path("/config/robotnikmq.yaml"),
            Path("/config/robotnikmq/robotnikmq.yaml"),
        ]
        if config:
            self.config = config
            log.debug(f"Config loaded from external source: {str(config)}")
        else:
            path = first(p for p in config_paths if p.exists())
            self.config = config_of(path)
            log.debug(f"Config loaded from {path}: {str(self.config)}")
        self._connection = None
        self._channel: Optional[BlockingChannel] = None
        self.log = log.bind(rmq_server="")

    @retry(stop=stop_after_attempt(3), wait=wait_random(0, 2),
           reraise=True, after=after_log(log, logging.WARN))
    @typechecked
    def _connect_to_server(self, config: ServerConfig) -> BlockingConnection:
        connection = BlockingConnection(config.conn_params())
        self.log = log.bind(rmq_server=f"{config.host}:{config.port}{config.vhost}")
        self.log.success(f"Connection to {config.host}:{config.port}{config.vhost} is successful")
        return connection

    @retry(stop=stop_after_attempt(2), reraise=True)
    @typechecked
    def _connect_to_cluster(self) -> BlockingConnection:
        self.log = log.bind(rmq_server="")
        for tier in self.config.tiers:
            for config in sample(tier, len(tier)):
                try:
                    return self._connect_to_server(config)
                except (AMQPError, OSError) as exc:
                    log.warning(f"Unable to connect to {config.host}:{config.port}{config.vhost}")
                    log.warning(exc)
        raise UnableToConnect(f"Cannot connect to any of the configured servers: {str(config)}")

    @property
    def connection(self) -> BlockingConnection:
        if self._connection is None or not self._connection.is_open:
            self._connection = self._connect_to_cluster()
        return self._connection

    @typechecked
    def _open_channel(self) -> BlockingChannel:
        _channel = self.connection.channel()
        _channel.basic_qos(prefetch_count=1)
        return _channel

    @property
    def channel(self) -> BlockingChannel:
        if self._channel is None or not self._channel.is_open:
            self._channel = self._open_channel()
        return self._channel

    @contextmanager
    def open_channel(self) -> Generator[BlockingChannel, None, None]:
        _ch = self.channel
        yield _ch
        self.close_channel(_ch)

    @typechecked
    def close_channel(self, channel: Optional[BlockingChannel] = None) -> None:
        channel = channel or self.channel
        if channel is not None and channel.is_open:
            channel.stop_consuming()
            channel.close()
