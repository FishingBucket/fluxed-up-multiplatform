__all__ = ["FluxerRateLimiter"]

from ...common.http.ratelimit import BucketKey, RateLimiter
from ...common.http.route import Route

MAJOR_PATHS = (
    "channel_id",
    "guild_id",
    "user_id",
    "stream_key",
    "invite_code",
    "client_id",
    "team_id",
    "pack_id",
    "target_id",
    "webhook_id",
)


class FluxerRateLimiter(RateLimiter):
    def get_bucket(self, route: Route) -> BucketKey:
        bucket = f"{route.meth} {route.path}"
        for key in MAJOR_PATHS:
            if key in route.parameters:
                bucket += f":{key}={route.parameters[key]}"
        return BucketKey(bucket)
