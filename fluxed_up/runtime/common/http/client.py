__all__ = ["HTTPClient"]

from asyncio import sleep
from typing import cast

from aiohttp import ClientError, ClientResponse, ClientSession, FormData

from ....exceptions import (
    BadRequest,
    Forbidden,
    GenericHTTPException,
    GenericNotFound,
    OperationException,
    RateLimited,
    Unauthorized,
)
from ....utils.types import JSON
from .ratelimit import RateLimiter
from .route import Route


class HTTPClient:
    """
    A somewhat generic implementation of an HTTP client to interact with a platform's REST API.
    """

    def __init__(
        self,
        auth_string: str,
        ratelimiter: RateLimiter,
        user_agent: str,
        max_retries: int = -1,
    ) -> None:
        self.auth_string = auth_string
        self.ratelimiter = ratelimiter
        self.max_retries = max_retries
        self.user_agent = user_agent

        self.session: ClientSession | None = None

    def get_session(self) -> ClientSession:
        if self.session is None or self.session.closed:
            self.session = ClientSession()
        return self.session

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    @classmethod
    def get_operation_exception_from_response(
        cls, response: ClientResponse
    ) -> OperationException:
        if response.status == 400:
            return BadRequest()
        elif response.status == 401:
            return Unauthorized()
        elif response.status == 403:
            return Forbidden()
        elif response.status == 404:
            return GenericNotFound()
        elif response.status == 429:
            return RateLimited()
        return GenericHTTPException(
            response.status, response.reason or "HTTP request failed"
        )

    async def request(
        self,
        route: Route,
        *,
        json: JSON = None,
        data: FormData | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> JSON:
        """
        Makes an HTTP request, respecting the token, ratelimits, and retries.

        Parameters
        ----------
        route : :class:`Route`
            The Route to make the request to.

        Other Parameters
        ----------------
        json : JSON, optional
            The JSON body to send.
        data : :class:`FormData`, optional
            The form data to send.
        params : dict[str, str], optional
            The query parameters to send.
        headers : dict[str, str], optional
            Any additional headers to add to the request.

        Returns
        -------
        JSON
            The response from the request.
        """

        session = self.get_session()
        request_headers = {
            "Authorization": self.auth_string,
            "User-Agent": self.user_agent,
        }
        if headers:
            request_headers |= headers

        attempts = 0
        bucket = self.ratelimiter.get_bucket(route)
        while True:
            async with self.ratelimiter.with_lock(bucket):
                retry_delay = 0.0
                try:
                    async with session.request(
                        route.meth,
                        route.url,
                        json=json,
                        data=data,
                        params=params,
                        headers=request_headers,
                    ) as response:
                        is_json = (
                            response.headers.get("Content-Type", None)
                            == "application/json"
                        )
                        if 200 <= response.status < 300:
                            if is_json:
                                return cast(JSON, await response.json(encoding="utf-8"))
                            text = await response.text(encoding="utf-8")
                            if not text:
                                return None
                            return text

                        if response.status == 429:
                            ratelimit_remaining = int(
                                response.headers.get("X-RateLimit-Remaining", 0)
                            )
                            if ratelimit_remaining == 0:
                                reset_after = float(
                                    response.headers.get("Retry-After", 0.2)
                                )
                                self.ratelimiter.deny(bucket, reset_after)
                            if response.headers.get("X-RateLimit-Global"):
                                reset_after = float(
                                    response.headers.get("Retry-After", 0.2)
                                )
                                self.ratelimiter.set_global(reset_after)

                except ClientError, TimeoutError:
                    retry_delay = 1.0 + attempts * 1.5

                if self.max_retries != -1 and attempts >= self.max_retries:
                    raise GenericHTTPException(-1, "")

                attempts += 1

                if retry_delay:
                    await sleep(retry_delay)
