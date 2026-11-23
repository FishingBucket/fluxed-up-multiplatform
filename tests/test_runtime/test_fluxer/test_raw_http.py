import pytest

from fluxed_up import ChannelID, GuildID, Platform
from fluxed_up.runtime.common.http.client import HTTPClient
from fluxed_up.runtime.common.http.route import Route, RouteMethod
from fluxed_up.runtime.fluxer.http.ratelimit import FluxerRateLimiter

AUTH = "Bot 1574307679239671808.w1RrwFIaX7mERYc2ZcJyOWi_jouKfr2654SzdptC1L0"
CHANNEL_ID = ChannelID(1574308337212719107, Platform.Fluxer)
GUILD_ID = GuildID(1574308337212719104, Platform.Fluxer)


@pytest.mark.asyncio
async def test_fetch() -> None:
    client = HTTPClient(
        AUTH, FluxerRateLimiter(), "fluxed-up-multiplatform (Fluxer/Python)", 3
    )
    route = Route(
        RouteMethod.GET,
        "/channels/{channel_id}",
        "https://fluxer.com/api/v1/",
        channel_id=str(CHANNEL_ID),
    )
    response = await client.request(route)
    assert isinstance(response, dict)
    assert response["id"] == str(CHANNEL_ID)
    assert response["guild_id"] == str(GUILD_ID)
    assert response["name"] == "general"
    await client.close()
