__all__ = ["BaseGatewayClient"]

import asyncio
from abc import ABC, abstractmethod
from typing import Literal

from aiohttp import (
    ClientError,
    ClientSession,
    ClientWebSocketResponse,
    WSMsgType,
    WSServerHandshakeError,
)

from ....exceptions import GenericGatewayException

type WebSocket = ClientWebSocketResponse[Literal[True]]


class BaseGatewayClient(ABC):
    """
    A skeleton of a gateway client. Wraps websockets.
    """

    def __init__(self, auth: str, gateway_url: str) -> None:
        self.auth = auth
        self.gateway_url = gateway_url
        self.ws: WebSocket | None = None
        self.session: ClientSession | None = None
        self.running = False

    @abstractmethod
    async def on_connect(self) -> None:
        """
        Code is run when the WebSocket is connected.
        """
        raise NotImplementedError

    @abstractmethod
    async def on_disconnect(self) -> None:
        """
        Code is run when the WebSocket is disconnected.
        """
        raise NotImplementedError

    @abstractmethod
    async def on_event(self, raw: bytes) -> None:
        """
        Code is run when the WebSocket receives a message from the server.

        Parameters
        ----------
        raw : bytes
            The raw bytes of the WebSocket message.
        """
        raise NotImplementedError

    @abstractmethod
    async def handle_close_code(self, close_code: int) -> None:
        """
        Code is run when the WebSocket is closed.

        Parameters
        ----------
        close_code : int
            The WebSocket's close code.
        """
        raise NotImplementedError

    @property
    def is_connected(self) -> bool:
        """
        Returns
        -------
        bool
            Whether the gateway is connected.
        """
        return self.session is not None and self.ws is not None and not self.ws.closed

    async def handle_loop(self) -> None:
        self.session = ClientSession()
        self.running = True

        try:
            while self.running:
                try:
                    await self.connect_run()
                except WSServerHandshakeError, ClientError, TimeoutError:
                    pass

                await asyncio.sleep(5)

        finally:
            await self.close()

    async def close(self) -> None:
        if self.ws and not self.ws.closed:
            await self.ws.close()

        if self.session and not self.session.closed:
            await self.session.close()

        self.running = False

    async def connect_run(self) -> None:
        assert self.session is not None
        self.ws = await self.session.ws_connect(self.gateway_url)
        await self.on_connect()

        try:
            await self.event_loop()
        finally:
            await self.on_disconnect()
            if self.ws and not self.ws.closed:
                await self.ws.close()

    async def event_loop(self) -> None:
        assert self.ws

        async for message in self.ws:
            if message.type in (WSMsgType.TEXT, WSMsgType.BINARY):
                raw: bytes = (
                    message.data
                    if message.type is WSMsgType.BINARY
                    else message.data.encode("utf-8")
                )
                await self.on_event(raw)

            elif (
                message.type in (WSMsgType.CLOSE, WSMsgType.CLOSING)
                or message.type is WSMsgType.ERROR
            ):
                break

        if self.ws.close_code:
            await self.handle_close_code(self.ws.close_code)

    async def send(self, data: str) -> None:
        if self.ws is None or self.ws.closed:
            raise GenericGatewayException("Cannot send on closed gateway.")
        await self.ws.send_str(data)
