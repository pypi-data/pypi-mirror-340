"""
Functions and objects related to the Configuration of RobotnikMQ
"""
from pathlib import Path
from random import choice
from ssl import create_default_context
from typing import Union, List, Optional, Dict, TypedDict, Annotated

from pika import ConnectionParameters, SSLOptions
from pika.credentials import PlainCredentials
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import AfterValidator
from pydantic.functional_serializers import PlainSerializer
from typeguard import typechecked
from yaml import safe_load

from robotnikmq.error import (
    NotConfigured,
    InvalidConfiguration,
)
from robotnikmq.log import log


@typechecked
def exists(path: Path) -> Path:
    assert path.exists()
    return Path(path).resolve(strict=True)


ExtantPath = Annotated[Path,
                       AfterValidator(exists),
                       PlainSerializer(lambda p: str(p), return_type=str, when_used='json')]


@typechecked
class ServerConfig(BaseModel):
    """
    Configuration object representing the configuration information required to connect to a single server
    """

    host: str
    port: int
    user: str
    password: str
    vhost: str
    ca_cert: Optional[ExtantPath] = None
    cert: Optional[ExtantPath] = None
    key: Optional[ExtantPath] = None
    _conn_params: Optional[ConnectionParameters] = None

    def conn_params(self) -> ConnectionParameters:
        if self._conn_params is not None:
            return self._conn_params
        if self.ca_cert is not None and self.cert is not None and self.key is not None:
            context = create_default_context(cafile=str(self.ca_cert))
            context.load_cert_chain(self.cert, self.key)
            return ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=PlainCredentials(self.user, self.password),
                ssl_options=SSLOptions(context, self.host),
            )
        context = create_default_context()
        return ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=PlainCredentials(self.user, self.password),
        )

    @staticmethod
    def from_connection_params(conn_params: ConnectionParameters) -> "ServerConfig":
        return ServerConfig(
            host=conn_params.host,
            port=conn_params.port,
            user=getattr(conn_params.credentials, "username", ""),
            password=getattr(conn_params.credentials, "password", ""),
            vhost=conn_params.virtual_host,
        )


@typechecked
def server_config(
    host: str,
    port: int,
    user: str,
    password: str,
    vhost: str,
    ca_cert: Union[str, Path, None] = None,
    cert: Union[str, Path, None] = None,
    key: Union[str, Path, None] = None,
) -> ServerConfig:
    """Generates a [`ServerConfig`][robotnikmq.config.ServerConfig] object while validating that the necessary certificate information.

    Args:
        host (str): Description
        port (int): Description
        user (str): Description
        password (str): Description
        vhost (str): Description
        ca_cert (Union[str, Path]): Description
        cert (Union[str, Path]): Description
        key (Union[str, Path]): Description
    """
    if ca_cert is not None and cert is not None and key is not None:
        ca_cert, cert, key = Path(ca_cert), Path(cert), Path(key)
        return ServerConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            vhost=vhost,
            ca_cert=ca_cert,
            cert=cert,
            key=key,
        )
    elif ca_cert is None and cert is None and key is None:
        return ServerConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            vhost=vhost,
        )
    else:
        raise InvalidConfiguration(
            "Either all public key encryption fields (cert, key, ca-cert) must be provided, or none of them."
        )


@typechecked
class RobotnikConfigTypedDict(TypedDict):
    tiers: List[List[Dict]]


@typechecked
class RobotnikConfig(BaseModel):
    tiers: List[List[ServerConfig]]

    def tier(self, index: int) -> List[ServerConfig]:
        return self.tiers[index]

    def a_server(self, tier: int) -> ServerConfig:
        return choice(self.tier(tier))

    def as_dict(self) -> RobotnikConfigTypedDict:
        return self.model_dump(mode='json')

    @staticmethod
    def from_tiered(
        tiers: List[List[ServerConfig]],
    ) -> "RobotnikConfig":
        return RobotnikConfig(tiers=tiers)

    @staticmethod
    def from_connection_params(conn_params: ConnectionParameters) -> "RobotnikConfig":
        return RobotnikConfig(
            tiers=[[ServerConfig.from_connection_params(conn_params)]]
        )


@typechecked
def config_of(config_file: Optional[Path]) -> RobotnikConfig:
    if config_file is None or not config_file.exists():
        log.critical("No valid RobotnikMQ configuration file was provided")
        raise NotConfigured("No valid RobotnikMQ configuration file was provided")
    return RobotnikConfig(**safe_load(config_file.open().read()))
