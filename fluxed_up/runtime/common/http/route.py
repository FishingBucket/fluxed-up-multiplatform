__all__ = ["Route", "RouteMethod"]

from enum import Enum
from urllib import parse


class RouteMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Route:
    """
    An HTTP request route.
    """

    __slots__ = ("base_url", "method", "parameters", "path")

    base_url: str
    method: RouteMethod
    parameters: dict[str, str]
    path: str

    def __init__(
        self, method: RouteMethod, path: str, base_url: str, **parameters: str
    ) -> None:
        self.method = method
        self.path = "/" + path.lstrip("/")
        self.base_url = base_url.rstrip("/")
        self.parameters = parameters

    @property
    def url(self) -> str:
        """
        Returns
        -------
        str
            The full URL of the Route plus its parameters.
        """
        encoded_parameters = {k: parse.quote(v) for k, v in self.parameters.items()}
        return f"{self.base_url}{self.path.format(**encoded_parameters)}"

    @property
    def meth(self) -> str:
        """
        Returns
        -------
        str
            The HTTP method of the route as a string.
        """
        return self.method.value
