from dataclasses import dataclass
from inspect import signature, Parameter
from json import loads as _from_json
from traceback import format_exc
from socket import gethostname
from typing import Optional, Callable, Union, Any, Dict, Tuple, List, TypedDict, Type
from typing import get_type_hints, get_origin, get_args
from uuid import uuid4 as uuid, UUID

from pika import BasicProperties
from pika.exceptions import AMQPError, ChannelError, AMQPConnectionError
from tenacity import retry, wait_exponential, retry_if_exception_type
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig
from robotnikmq.core import Robotnik, thread_name, valid_json
from robotnikmq.utils import to_json as _to_json
from robotnikmq.log import log


@typechecked
def _type_hint_str(typ: Any) -> str:
    if get_origin(typ) is Union:
        return f"Union[{','.join([_type_hint_str(t) for t in get_args(typ)])}]"
    return str(typ.__name__)

@typechecked
class RpcErrorTypedDict(TypedDict):
    request_id: str
    type: str
    details: Union[None, str, Dict[str, Any]]

@typechecked
@dataclass(frozen=True)
class RpcError:
    request_id: Union[str, UUID]
    details: Union[None, str, Dict[str, Any]]

    @staticmethod
    def of(
        request_id: Union[str, UUID, None] = None,
        details: Union[None, str, Dict[str, Any]] = None,
    ) -> 'RpcError':
        return RpcError(request_id or uuid(), details)

    def to_json(self) -> str:
        return _to_json(self.to_dict())

    def to_dict(self) -> RpcErrorTypedDict:
        return {
            "request_id": str(self.request_id),
            "type": "error",
            "details": self.details,
        }

    @staticmethod
    def from_json(json_str: Union[str, bytes]) -> Optional['RpcError']:
        json_str = json_str if isinstance(json_str, str) else json_str.decode()
        log.debug(json_str)
        if valid_json(json_str):
            data = _from_json(json_str)
            if all(k in data for k in {"request_id", "type", "details"}):
                return RpcError.of(request_id=data["request_id"], details=data["details"])
        return None


@typechecked
class RpcResponseTypedDict(TypedDict):
    request_id: str
    type: str
    data: Union[None, str, int, float, Dict[str, Any], List[Dict[str, Any]]]


@typechecked
@dataclass(frozen=True)
class RpcResponse:
    request_id: Union[str, UUID]
    data: Union[None, str, int, float, Dict[str, Any], List[Dict[str, Any]]]

    @staticmethod
    def of(
        request_id: Union[str, UUID, None] = None,
        data: Union[None, str, int, float, Dict[str, Any], List[Dict[str, Any]]] = None,
    ) -> 'RpcResponse':
        return RpcResponse(request_id or uuid(), data)

    def to_dict(self) -> RpcResponseTypedDict:
        return {
            "request_id": str(self.request_id),
            "type": "response",
            "data": self.data,
        }

    def to_json(self) -> str:
        return _to_json(self.to_dict())

    @staticmethod
    def from_json(json_str: Union[str, bytes]) -> Optional["RpcResponse"]:
        json_str = json_str if isinstance(json_str, str) else json_str.decode()
        if valid_json(json_str):
            data = _from_json(json_str)
            if all(k in data for k in ("request_id", "type", "data")):
                return RpcResponse.of(request_id=data["request_id"], data=data["data"])
        return None


class RpcServer(Robotnik):
    @typechecked
    def __init__(
        self,
        config: Optional[RobotnikConfig] = None,
        meta_queue_prefix: Optional[str] = None,
        docs_queue_suffix: Optional[str] = None,
        only_once: bool = False,
    ):
        super().__init__(config=config)
        self._callbacks: Dict[str, Callable] = {}
        self.meta_queue_prefix = meta_queue_prefix or gethostname()
        self.docs_queue_suffix = docs_queue_suffix or ".__doc__"
        # Typically used for testing, implies server should stop after 1 response
        self.only_once = only_once

    @typechecked
    def _register_docs(self, queue: str, callback: Callable) -> None:
        self.channel.queue_declare(
            queue=queue + self.docs_queue_suffix, exclusive=False
        )

        @typechecked
        def docs_callback(_, method, props: BasicProperties, __) -> None:
            req_id = props.correlation_id or uuid()
            response = RpcResponse.of(
                req_id,
                data={
                    "rpc_queue": queue,
                    "inputs": self._get_input_type_strings(queue),
                    "returns": self._get_return_type_str(queue),
                    "description": callback.__doc__,
                },
            )
            self.channel.basic_publish(
                exchange="",
                routing_key=props.reply_to or "",
                properties=BasicProperties(correlation_id=props.correlation_id),
                body=response.to_json(),
            )
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue=queue + self.docs_queue_suffix,
            on_message_callback=docs_callback,
            auto_ack=False,
        )

    @typechecked
    def _get_defaults(self, queue: str) -> Dict:
        params = signature(self._callbacks[queue]).parameters
        return {
            p: params[p].default
            for p in params
            if params[p].default is not Parameter.empty
        }

    @typechecked
    def _get_input_types(self, queue: str) -> Dict:
        return {
            k: v
            for k, v in get_type_hints(self._callbacks[queue]).items()
            if k != "return"
        }

    @typechecked
    def _get_input_type_strings(self, queue: str) -> Dict:
        return {
            k: _type_hint_str(v)
            for k, v in get_type_hints(self._callbacks[queue]).items()
            if k != "return"
        }

    @typechecked
    def _get_return_type_str(self, queue: str) -> Any:
        return _type_hint_str(get_type_hints(self._callbacks[queue])["return"])

    @typechecked
    @staticmethod
    def _is_optional(arg_type: Any) -> bool:
        return get_origin(arg_type) is Union and type(None) in get_args(arg_type)

    @typechecked
    @staticmethod
    def _valid_arg(arg_value: Any, arg_type: Any) -> bool:
        if arg_type is Any:
            return True
        if get_origin(arg_type) is Union:
            if (type(None) in get_args(arg_type)) and (
                arg_value is None or arg_value == {}
            ):  # Optional
                return True
            return any(
                RpcServer._valid_arg(arg_value, typ) for typ in get_args(arg_type)
            )
        if get_origin(arg_type) is dict:
            key_type, val_type = get_args(arg_type)
            return all(
                RpcServer._valid_arg(key, key_type) for key in arg_value.keys()
            ) and all(RpcServer._valid_arg(val, val_type) for val in arg_value.values())
        return isinstance(arg_value, arg_type)

    def _valid_inputs(self, queue: str, inputs: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        inputs_with_defaults = {**self._get_defaults(queue), **inputs}
        for arg_name, arg_type in self._get_input_types(queue).items():
            if arg_name not in inputs_with_defaults and not self._is_optional(arg_type):
                return False, f"Missing required argument {arg_name}"
            if arg_name in inputs_with_defaults and not self._valid_arg(
                inputs_with_defaults[arg_name], arg_type
            ):
                return False, f"Invalid type for {arg_name}"
        return True, None

    @typechecked
    def register_rpc(
        self, queue: str, callback: Callable, register_docs: bool = True
    ) -> None:
        self.channel.queue_declare(queue=queue, exclusive=False)
        self._callbacks[queue] = callback
        if register_docs:
            self._register_docs(queue, callback)
        # TODO: servers should have an exclusive Queue for information about themselves

        @typechecked
        def meta_callback(_, method, props: BasicProperties, body: bytes):
            req_id = props.correlation_id or uuid()
            with thread_name(req_id):
                self.log.debug("Request received")
                try:
                    try:
                        if valid_json(body.decode()):
                            input_args: Dict = _from_json(body.decode())
                            self.log.debug(f"Input JSON is valid: {input_args}")
                            valid_inputs, msg = self._valid_inputs(queue, input_args)
                            if not valid_inputs:
                                self.log.debug("Invalid input")
                                response = RpcError.of(req_id, msg).to_json()
                            elif not input_args:
                                self.log.debug(f"Executing: {callback}")
                                response = RpcResponse.of(req_id, callback()).to_json()
                            else:
                                self.log.debug(
                                    f"Executing: {callback} with inputs: {input_args}"
                                )
                                response = RpcResponse.of(
                                    req_id, callback(**input_args)
                                ).to_json()
                        else:
                            response = RpcError.of(
                                req_id, "Input could not be decoded as JSON"
                            ).to_json()
                    except (AMQPError, ChannelError):
                        raise  # we want this kind of exception to be caught further down
                    except Exception:  # pylint: disable=W0703
                        self.log.error(
                            "An error has occurred during the execution of the RPC method"
                        )
                        for line in format_exc().split("\n"):
                            self.log.error(line)
                        response = RpcError.of(
                            request_id=req_id,
                            details=f"There was an error "
                            f"while processing the "
                            f"request, please refer "
                            f"to server log with "
                            f"request ID: "
                            f"{req_id}",
                        ).to_json()
                    self.log.debug(f"Response: {response}")
                    self.channel.basic_publish(
                        exchange="",
                        routing_key=props.reply_to or "",
                        properties=BasicProperties(correlation_id=props.correlation_id),
                        body=response,
                    )
                    self.channel.basic_ack(delivery_tag=method.delivery_tag)
                    self.log.debug("Response sent and ack-ed")
                except (AMQPError, ChannelError):
                    self.log.error(
                        f"A RabbitMQ communication error has occurred while processing "
                        f"Request ID: {req_id}"
                    )
                    for line in format_exc().split("\n"):
                        self.log.error(line)
            if self.only_once:
                self.channel.stop_consuming()

        self.channel.basic_consume(
            queue=queue, on_message_callback=meta_callback, auto_ack=False
        )

    @retry(
        retry=retry_if_exception_type((AMQPConnectionError, OSError)),
        wait=wait_exponential(multiplier=1, min=3, max=30),
    )
    @typechecked
    def run(self) -> None:
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.log.info("Shutting down server")
