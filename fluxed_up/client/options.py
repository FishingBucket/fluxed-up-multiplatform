__all__ = ["CacheOptions", "CacheStrategy"]

from dataclasses import dataclass
from enum import IntFlag, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client  # noqa # used in docs


class CacheStrategy(IntFlag):
    """
    Strategies on how a :class:`Client` should cache a specific type of API resource.
    """

    ON_EVENT = auto()
    """
    The Client will fetch and cache this resource when an event that corresponds to this fires.
    """
    ON_EXPLICIT_FETCH = auto()
    """
    The Client will only cache the resource when the code explicitly fetches a resource.
    """

    @classmethod
    def no_auto(cls) -> CacheStrategy:
        return cls(0)

    @classmethod
    def all(cls) -> CacheStrategy:
        return cls.ON_EVENT | cls.ON_EXPLICIT_FETCH


@dataclass(frozen=True)
class SingleCache:
    """
    Configuration for a single resource type cache.
    """

    max: int
    """
    The maximum number of this resource type to keep in the cache. Negative numbers indicate no limit.
    """
    strategy: CacheStrategy
    """
    The strategy to use when trying to automatically caching this resource.
    """


@dataclass(kw_only=True, frozen=True)
class CacheOptions:
    """
    A dataclass to configure how a :class:`Client` should cache API data.
    """

    messages = SingleCache(1024, CacheStrategy.all())
    members = SingleCache(1024, CacheStrategy.ON_EXPLICIT_FETCH)
    users = SingleCache(2048, CacheStrategy.ON_EXPLICIT_FETCH)
    guilds = SingleCache(-1, CacheStrategy.all())
    channels = SingleCache(-1, CacheStrategy.all())
