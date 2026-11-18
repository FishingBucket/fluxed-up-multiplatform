__all__ = ["Client"]

from .options import CacheOptions


class Client:
    """
    A Client to connect and act as an agent on a platform.

    Other Parameters
    ----------------
    cache : :class:`CacheOptions`, optional
        Configuration for how the Client should cache certain API data.
    """

    def __init__(self, *, cache: CacheOptions = None) -> None:
        self.cache = cache or CacheOptions()
