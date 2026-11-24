import os

import pytest
from dotenv import load_dotenv

load_dotenv()

from fluxed_up import ChannelID, GuildID, Platform, Token
from fluxed_up.runtime.common.http.client import HTTPClient
from fluxed_up.runtime.common.http.route import Route, RouteMethod
from fluxed_up.runtime.fluxer.http.ratelimit import FluxerRateLimiter

AUTH = f"Bot {Token.from_env().get_token()}"
CHANNEL_ID = ChannelID(os.environ["CHANNEL"], Platform.Fluxer)
GUILD_ID = GuildID(os.environ["GUILD"], Platform.Fluxer)


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
