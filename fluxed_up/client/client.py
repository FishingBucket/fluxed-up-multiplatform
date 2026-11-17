__all__ = ["Client"]

from typing import TYPE_CHECKING

from .options import CacheOptions

if TYPE_CHECKING:
    from ..platform import Platform  # noqa # used for docs


class Client:
    """
    A Client to connect and act as an agent on a platform.

    Attributes
    ----------
    platform : :class:`Platform`
        The platform this Client is connected to.

    Other Parameters
    ----------------
    cache : :class:`CacheOptions`, optional
        Configuration for how the Client should cache certain API data.
    """

    platform = Platform.Auto

    def __init__(self, *, cache: CacheOptions = None) -> None:
        self.cache = cache or CacheOptions()
