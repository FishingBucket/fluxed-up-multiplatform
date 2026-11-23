__all__ = ["BucketKey", "RateLimiter"]

from abc import ABC, abstractmethod
from asyncio import Lock, get_running_loop, sleep
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import NewType

from .route import Route

BucketKey = NewType("BucketKey", str)


# Modification of
# https://github.com/Fluxer-py/fluxer.py/blob/rework/fluxer/http.py#L175-L303
class RateLimiter(ABC):
    # can someone tell me what the fuck is going on in the original???

    """
    An abstract class to manage rate limits.
    """

    def __init__(self) -> None:
        self.locks: dict[BucketKey, Lock] = {}
        self.reset_times: dict[BucketKey, float] = {}
        self.globally_ratelimited_until = 0.0

    @abstractmethod
    def get_bucket(self, route: Route) -> BucketKey:
        """
        Get the bucket key for the given route.

        Parameters
        ----------
        route : :class:`Route`
            The route to calculate the bucket key from.

        Returns
        -------
        BucketKey
            The resolved BucketKey.
        """
        raise NotImplementedError

    def get_lock(self, key: BucketKey) -> Lock:
        """
        Get the lock for the given key, creating it if necessary.

        Parameters
        ----------
        key : BucketKey
            The bucket key to get.

        Returns
        -------
        :class:`Lock`
            The asyncio Lock object.
        """
        return self.locks.setdefault(key, Lock())

    async def acquire(self, bucket: BucketKey) -> None:
        """
        Waits and acquires a lock on a bucket.

        Parameters
        ----------
        bucket : :class:`BucketKey`
            The bucket to acquire.
        """
        lock = self.get_lock(bucket)
        await lock.acquire()
        try:
            sleep_until = max(
                self.globally_ratelimited_until, self.reset_times.get(bucket, 0)
            )
            delay = sleep_until - get_running_loop().time()
            if delay > 0:
                await sleep(delay)
        except BaseException:
            self.release(bucket)
            raise

    def release(self, bucket: BucketKey) -> None:
        """
        Releases a lock on a bucket.

        Parameters
        ----------
        bucket : BucketKey
            The bucket to release.
        """
        lock = self.get_lock(bucket)
        if lock.locked():
            lock.release()

    @asynccontextmanager
    async def with_lock(self, bucket: BucketKey) -> AsyncGenerator[None]:
        """
        A context manager to deal with bucket acquiring and releasing.

        Parameters
        ----------
        bucket : BucketKey
            The bucket key to use.
        """
        await self.acquire(bucket)
        try:
            yield
        finally:
            self.release(bucket)

    def set_global(self, reset_after: float) -> None:
        """
        Sets the global ratelimit.

        Parameters
        ----------
        reset_after : float
            The time in seconds until the global ratelimit expires.
        """
        self.globally_ratelimited_until = max(
            get_running_loop().time() + reset_after, self.globally_ratelimited_until
        )

    def deny(self, bucket: BucketKey, retry_after: float) -> None:
        """
        Initiate a ratelimit.

        Parameters
        ----------
        bucket : BucketKey
            The bucket key that is ratelimited.
        retry_after : float
            The time in seconds that this bucket is ratelimited.
        """
        self.reset_times[bucket] = max(
            self.reset_times.get(bucket, 0), get_running_loop().time() + retry_after
        )
