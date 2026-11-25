import asyncio
from typing import cast

from dotenv import load_dotenv

from fluxed_up import Token
from fluxed_up.runtime.common.gateway.common_client import (
    CommonGatewayClient,
    GatewayPayload,
    IdentifyInformation,
)

load_dotenv()

AUTH = Token.from_env().get_token()


async def handle_dispatch(
    client: CommonGatewayClient, dispatch: GatewayPayload
) -> None:
    print(dispatch)
    if dispatch["t"] == "MESSAGE_CREATE":
        data = cast(dict[str, str], dispatch["d"])
        if data["content"] == "ping":
            print(client.latency)


async def main() -> None:
    client = CommonGatewayClient(
        AUTH,
        "wss://gateway.fluxer.com?v=1",
        IdentifyInformation("Python 3.14"),
        lambda data: handle_dispatch(client, data),
    )
    await client.handle_loop()


asyncio.run(main())
