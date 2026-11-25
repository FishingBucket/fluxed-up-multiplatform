import asyncio
import json
import os
from collections.abc import AsyncGenerator

import pytest
from aioresponses import aioresponses
from dotenv import load_dotenv

from fluxed_up import ChannelID, GuildID, Platform, Token
from fluxed_up.exceptions import GenericNotFound
from fluxed_up.runtime.common.http.client import HTTPClient
from fluxed_up.runtime.common.http.route import Route, RouteMethod
from fluxed_up.runtime.fluxer.http.ratelimit import FluxerRateLimiter

load_dotenv()

AUTH = f"Bot {Token.from_env().get_token()}"
CHANNEL_ID = ChannelID(os.environ["CHANNEL"], Platform.Fluxer)
GUILD_ID = GuildID(os.environ["GUILD"], Platform.Fluxer)

TEST_CONTENT = "test message"


@pytest.fixture
async def client() -> AsyncGenerator[HTTPClient]:
    client = HTTPClient(
        AUTH, "https://fluxer.com/api/v1/", FluxerRateLimiter(), "fluxed-up-multiplatform (Fluxer/Python)", 3
    )
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_fetch(client: HTTPClient) -> None:
    route = Route(
        RouteMethod.GET,
        "/channels/{channel_id}",
        channel_id=str(CHANNEL_ID),
    )
    response = await client.request(route)
    assert isinstance(response, dict)
    assert response["id"] == str(CHANNEL_ID)
    assert response["guild_id"] == str(GUILD_ID)
    assert response["name"] == "general"


@pytest.mark.asyncio
async def test_error(client: HTTPClient) -> None:
    route = Route(
        RouteMethod.GET,
        "/channels/{channel_id}",
        channel_id=str(CHANNEL_ID.id + 10),  # this ID does not exist trust me
    )
    with pytest.raises(GenericNotFound):
        await client.request(route)


@pytest.mark.asyncio
async def test_send(client: HTTPClient) -> None:
    route = Route(
        RouteMethod.POST,
        "/channels/{channel_id}/messages",
        channel_id=str(CHANNEL_ID.id),
    )
    response = await client.request(
        route,
        json={
            "content": TEST_CONTENT,
        },
    )
    assert isinstance(response, dict)
    assert response["content"] == TEST_CONTENT


@pytest.mark.asyncio
async def test_ratelimit(client: HTTPClient) -> None:
    route = Route(
        RouteMethod.POST,
        "/channels/{channel_id}/messages",
        channel_id=str(CHANNEL_ID.id),
    )

    url = route.url(client.base_url)

    with aioresponses() as mock:
        mock.post(
            url,
            status=429,
            headers={
                "Retry-After": "2",
                "X-RateLimit-Remaining": "0",
                "Content-Type": "application/json",
            },
            body=json.dumps(
                {
                    "message": "You are being rate limited.",
                    "retry_after": 2,
                    "global": False,
                }
            ),
        )
        mock.post(
            url,
            status=200,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"id": "100", "content": TEST_CONTENT}),
        )
        time_start = asyncio.get_running_loop().time()
        response = await client.request(route, json={"content": TEST_CONTENT})
        time_end = asyncio.get_running_loop().time()
        assert time_end - time_start > 2
        assert isinstance(response, dict)
        assert response["content"] == TEST_CONTENT
