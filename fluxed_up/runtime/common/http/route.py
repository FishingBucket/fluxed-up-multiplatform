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

    base_url: str | None
    method: RouteMethod
    parameters: dict[str, str]
    path: str

    def __init__(
        self,
        method: RouteMethod,
        path: str,
        base_url: str | None = None,
        **parameters: str,
    ) -> None:
        self.method = method
        self.path = "/" + path.lstrip("/")
        self.base_url = base_url.rstrip("/") if base_url else None
        self.parameters = parameters

    def url(self, base_url: str | None = None) -> str:
        """
        Generates the full URL for the route.

        Parameters
        ----------
        base_url : str | None
            The base URL for the route, overriding the Route default.

        Returns
        -------
        str
            The full URL of the Route plus its parameters.

        Raises
        ------
        ValueError
            If neither the Route base URL nor this base URL are provided.
        """
        encoded_parameters = {k: parse.quote(v) for k, v in self.parameters.items()}
        if not self.base_url and not base_url:
            raise ValueError(
                "Either the Route must have a base_url or the url() method must have a base_url."
            )

        return f"{
            self.base_url or base_url.rstrip('/')  # type: ignore
        }{self.path.format(**encoded_parameters)}"

    @property
    def meth(self) -> str:
        """
        Returns
        -------
        str
            The HTTP method of the route as a string.
        """
        return self.method.value
