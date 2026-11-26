__all__ = ["CommonClient"]

import time

from ....client import Client, ClientGhost
from ....exceptions import ResourceNotInitialized
from ....models.channels.channels import Channel, ChannelID
from ....models.guilds.guilds import Guild, GuildID
from ....models.messages.messages import Message, MessageRef
from ....models.session import SessionContext
from ....models.users import User, UserID
from ....token import Token
from ..endpoints import Endpoints
from ..gateway.common_client import CommonGatewayClient, IdentifyInformation
from ..http.client import HTTPClient
from ..http.route import Route, RouteMethod


class CommonClient[
    ThisGatewayClient: CommonGatewayClient = CommonGatewayClient,
    ThisHTTPClient: HTTPClient = HTTPClient,
](Client):
    def __init__(
        self,
        identify: IdentifyInformation,
        endpoints: Endpoints,
        client_ghost: ClientGhost,
        context: SessionContext,
    ) -> None:
        super().__init__(client_ghost, context)
        self.identify = identify
        self.endpoints = endpoints

        self.gateway: ThisGatewayClient | None = None
        self.http: ThisHTTPClient | None = None

    def _assert_initialized(self) -> tuple[ThisGatewayClient, ThisHTTPClient]:
        if self.gateway is None:
            raise ResourceNotInitialized("GatewayClient")
        if self.http is None:
            raise ResourceNotInitialized("HTTPClient")
        return self.gateway, self.http

    async def run(self, token: Token) -> None:
        pass

    @property
    def latency(self) -> float:
        gateway, _ = self._assert_initialized()
        return gateway.latency

    async def get_http_latency(self) -> float:
        _, http = self._assert_initialized()
        start = time.perf_counter()
        await http.request(Route(RouteMethod.GET, "/"))
        end = time.perf_counter()
        return end - start

    @property
    def guilds(self) -> list[Guild]:
        pass

    async def get_guild(self, guild_id: GuildID) -> Guild:
        pass

    async def get_channel(self, channel_id: ChannelID) -> Channel:
        pass

    async def get_user(self, user_id: UserID) -> User:
        pass

    async def get_message(self, ref: MessageRef) -> Message:
        pass
