"""Authentication Middlewares."""

from .base import SyncHTTPAddHeadersMiddleware


class SyncHTTPAuthorizationMiddleware(SyncHTTPAddHeadersMiddleware):
    """
    Authentication Mechanism based on the header `Authorization`.

    :param scheme: the scheme of the mechanism.
    :param value: the value that authenticate the user using the scheme.
    """

    def __init__(self, scheme: str, value: str):
        return super().__init__({"Authorization": f"{scheme} {value}"})


class SyncHTTPBearerMiddleware(SyncHTTPAuthorizationMiddleware):
    """
    Authentication Mechanism based on the header `Authorization` with the Bearer scheme.

    :param value: value of the bearer token.
    """

    def __init__(self, bearer_token: str):
        return super().__init__("Bearer", bearer_token)
