"""
The discovery based on :term:`Consul`.

This driver implement a client side service discovery.
"""

import random
from typing import Any, Callable, Optional

from pydantic.fields import Field
from result import Result

from blacksmith.domain.exceptions import HTTPError, UnregisteredServiceException
from blacksmith.domain.model import PathInfoField, Request, Response
from blacksmith.domain.model.params import CollectionIterator
from blacksmith.domain.registry import Registry
from blacksmith.middleware._sync.auth import SyncHTTPBearerMiddleware
from blacksmith.sd._sync.adapters.static import SyncStaticDiscovery
from blacksmith.sd._sync.base import SyncAbstractServiceDiscovery, Url
from blacksmith.service._sync.client import SyncClientFactory
from blacksmith.typing import ServiceName, Version


class ConsulApiError(HTTPError):
    """Raised when consul API is not responding what is expected."""

    def __init__(self, exc: HTTPError):
        return super().__init__(str(exc), exc.request, exc.response)


class ServiceRequest(Request):
    """Request parameter of the Consul API to retrieve a host for a service."""

    name: str = PathInfoField()
    """Name of the service to search for an endpoint."""


class Service(Response):
    """Consul Service response."""

    node_address: str = Field(alias="Address")
    """IP address of the Consul node on which the service is registered."""
    service_address: Optional[str] = Field(default=None, alias="ServiceAddress")
    """IP address of the service host. if empty, node address is used."""
    port: int = Field(alias="ServicePort")
    """TCP Port of an instance that host the service."""

    @property
    def address(self) -> str:
        return self.service_address or self.node_address


_registry = Registry()
_registry.register(
    "consul",
    "services",
    "consul",
    "v1",
    collection_path="/catalog/service/{name}",
    collection_contract={"GET": (ServiceRequest, Service)},
)


def blacksmith_cli(endpoint: Url, consul_token: str) -> SyncClientFactory[HTTPError]:
    sd = SyncStaticDiscovery({("consul", "v1"): endpoint})
    fact: SyncClientFactory[HTTPError] = SyncClientFactory(sd, registry=_registry)
    if consul_token:
        fact.add_middleware(SyncHTTPBearerMiddleware(consul_token))
    return fact


class SyncConsulDiscovery(SyncAbstractServiceDiscovery):
    """
    A discovery instance based on a :term:`Consul` server.

    :param addr: endpoint of the consul v1 http api.
    :param service_name_fmt: pattern for name of versionned service.
    :param service_url_fmt: pattern for url of versionned service.
    :param unversioned_service_name_fmt: pattern for name of unversioned service.
    :param unversioned_service_url_fmt: pattern for url of unversioned service.
    :param consul_token: If set, the consul token is sent on http api call.
    """

    addr: str
    service_name_fmt: str
    service_url_fmt: str
    unversioned_service_name_fmt: str
    unversioned_service_url_fmt: str
    consul_token: str

    def __init__(
        self,
        addr: Url = "http://consul:8500/v1",
        service_name_fmt: str = "{service}-{version}",
        service_url_fmt: str = "http://{address}:{port}/{version}",
        unversioned_service_name_fmt: str = "{service}",
        unversioned_service_url_fmt: str = "http://{address}:{port}",
        consul_token: str = "",
        _client_factory: Callable[[Url, str], SyncClientFactory[Any]] = blacksmith_cli,
    ) -> None:
        self.blacksmith_cli = _client_factory(addr, consul_token)
        self.service_name_fmt = service_name_fmt
        self.service_url_fmt = service_url_fmt
        self.unversioned_service_name_fmt = unversioned_service_name_fmt
        self.unversioned_service_url_fmt = unversioned_service_url_fmt

    def format_service_name(self, service: ServiceName, version: Version) -> str:
        """Build the service name to send to consul."""
        if version is None:
            name = self.unversioned_service_name_fmt.format(service=service)
        else:
            name = self.service_name_fmt.format(service=service, version=version)
        return name

    def format_endoint(self, version: Version, address: str, port: int) -> Url:
        """Build the rest api endpoint from consul response."""
        if version is None:
            endpoint = self.unversioned_service_url_fmt.format(
                address=address, port=port
            )
        else:
            endpoint = self.service_url_fmt.format(
                version=version, address=address, port=port
            )
        return endpoint

    def resolve(self, service: ServiceName, version: Version) -> Service:
        """
        Get the :class:`Service` from the consul registry.

        If many instances host the service, the host is choosen randomly.
        """
        name = self.format_service_name(service, version)
        consul = self.blacksmith_cli("consul")
        rresp: Result[CollectionIterator[Service], HTTPError] = (
            consul.services.collection_get(ServiceRequest(name=name))
        )
        if rresp.is_err():
            raise ConsulApiError(
                rresp.unwrap_err()
            )  # rewrite the class to avoid confusion
        else:
            resp: list[Service] = list(rresp.unwrap())
            if not resp:
                raise UnregisteredServiceException(service, version)
            return random.choice(resp)

    def get_endpoint(self, service: ServiceName, version: Version) -> Url:
        """
        Get the endpoint from the consul registry

        If many instances host the service, the host is choosen randomly.
        """
        srv = self.resolve(service, version)
        return self.format_endoint(version, srv.address, srv.port)
