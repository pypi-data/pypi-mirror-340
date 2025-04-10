"""
The discovery to start simple.

The static discovery strategy is a good start when you don't need a strategy.

For instance, a short list of services with static endpoint.
"""

from collections.abc import Mapping

from blacksmith.domain.exceptions import UnregisteredServiceException
from blacksmith.typing import Service, ServiceName, Version

from ..base import AsyncAbstractServiceDiscovery, Url

Endpoints = Mapping[Service, Url]


class AsyncStaticDiscovery(AsyncAbstractServiceDiscovery):
    """
    A discovery instance based on a static dictionary.
    """

    endpoints: Endpoints

    def __init__(self, endpoints: Endpoints) -> None:
        self.endpoints = endpoints

    async def get_endpoint(self, service: ServiceName, version: Version) -> Url:
        """
        Retrieve endpoint using the given parameters from `endpoints`.
        """
        try:
            return self.endpoints[(service, version)]
        except KeyError as exc:
            raise UnregisteredServiceException(service, version) from exc
