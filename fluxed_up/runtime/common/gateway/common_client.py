__all__ = [
    "CommonGatewayClient",
    "GatewayOp",
    "GatewayPayload",
    "IdentifyInformation",
    "ShardID",
]

import asyncio
import json
import sys
import time
from asyncio import Task
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import NewType, NotRequired, TypedDict, cast

from ....models.intents import Intents
from ....utils.types import JSON
from .client import BaseGatewayClient

GatewayOp = NewType("GatewayOp", int)


class GatewayPayload(TypedDict):
    """
    A payload through the gateway.
    """

    op: GatewayOp
    d: NotRequired[JSON]
    s: NotRequired[int]
    t: NotRequired[str]


ShardID = NewType("ShardID", str)


@dataclass
class IdentifyInformation:
    """
    Data about this application and the gateway session.
    """

    device: str
    intents: Intents = field(default=Intents.default())
    shard: ShardID | None = None
    total_shards: int = 0


class CommonGatewayClient(BaseGatewayClient):
    """
    Common gateway client implementing a Discord-ish gateway protocol.
    """

    DISPATCH = GatewayOp(0)
    HEARTBEAT = GatewayOp(1)
    IDENTIFY = GatewayOp(2)
    RESUME = GatewayOp(6)
    DISCONNECT = GatewayOp(7)
    INVALID_SESSION = GatewayOp(9)
    HELLO = GatewayOp(10)
    HEARTBEAT_ACK = GatewayOp(11)

    def __init__(
        self,
        auth: str,
        gateway_url: str,
        identify: IdentifyInformation,
        handle_dispatch: Callable[[GatewayPayload], Coroutine[None, None, None]],
    ):
        super().__init__(auth, gateway_url)
        self.identify_info = identify
        self.handle_dispatch = handle_dispatch

        self.heartbeat_interval: float = 0
        self.latency: float = float("inf")
        self.session_id: str | None = None
        self.sequence: int | None = None

        self.disconnected_time: float | None = None

        self.last_heartbeat: float = 0
        self.heartbeat_loop: Task[None] | None = None
        self.last_heartbeat_ack = False

        self.tasks: list[Task[None]] = []

    async def on_connect(self) -> None:
        if (
            self.disconnected_time
            and (asyncio.get_running_loop().time() - self.disconnected_time) >= 60
        ):
            self.session_id = None
            self.sequence = None
            self.latency = float("inf")

    async def on_disconnect(self) -> None:
        await self.stop_heartbeat()
        self.disconnected_time = asyncio.get_running_loop().time()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def on_event(self, raw: bytes) -> None:
        data = json.loads(raw.decode("utf-8"))
        await self.event(data)

    async def handle_close_code(self, close_code: int) -> None:
        if close_code in (4007, 4009):
            self.session_id = None
            self.sequence = 0

        if close_code in (4004, 4010, 4011, 4012, 4013, 4014):
            self.running = False

    async def event(self, data: GatewayPayload) -> None:
        if data["op"] == self.HELLO:
            self.heartbeat_interval = (
                cast(
                    float,
                    data["d"]["heartbeat_interval"],  # type: ignore
                )
                / 1000
            )
            await self.start_heartbeat()
            if self.session_id:
                await self.resume()
            else:
                await self.identify()

        elif data["op"] == self.HEARTBEAT_ACK:
            self.last_heartbeat_ack = True
            self.latency = time.perf_counter() - self.last_heartbeat

        elif data["op"] == self.HEARTBEAT:
            await self.send_heartbeat()

        elif data["op"] == self.DISPATCH:
            if data["s"] is not None:
                self.sequence = data["s"]

            await self.on_dispatch(data)

        elif data["op"] == self.DISCONNECT and self.ws and not self.ws.closed:
            await self.ws.close()

        elif data["op"] == self.INVALID_SESSION:
            resumable = data["d"] if isinstance(data["d"], bool) else False
            if not resumable:
                self.session_id = None
                self.sequence = 0
            if self.ws:
                await self.ws.close()

    async def send_payload(self, payload: GatewayPayload) -> None:
        data = json.dumps(payload)
        if len(data) >= 4096:
            raise ValueError("Payload too large")
        await self.send(data)

    async def identify(self) -> None:
        data: dict[str, JSON] = {
            "token": self.auth,
            "properties": {
                "os": sys.platform,
                "browser": "fluxed-up-multiplatform",
                "device": self.identify_info.device,
            },
            "intents": int(self.identify_info.intents),
        }
        if self.identify_info.shard is not None:
            data |= {
                "shard": [self.identify_info.shard, self.identify_info.total_shards],
            }
        await self.send_payload(
            {
                "op": self.IDENTIFY,
                "d": data,
            }
        )

    async def resume(self) -> None:
        await self.send_payload(
            {
                "op": self.RESUME,
                "d": {
                    "token": self.auth,
                    "session_id": self.session_id,
                    "seq": self.sequence,
                },
            }
        )

    async def start_heartbeat(self) -> None:
        await self.stop_heartbeat()
        self.last_heartbeat = 0
        self.last_heartbeat_ack = True
        self.latency = float("inf")

        async def heartbeat_loop() -> None:
            try:
                while True:
                    if not self.is_connected:
                        return
                    if not self.last_heartbeat_ack:
                        if self.ws and not self.ws.closed:
                            await self.ws.close(code=4000)
                        return

                    self.last_heartbeat_ack = False
                    await self.send_heartbeat()
                    await asyncio.sleep(self.heartbeat_interval)
            except asyncio.CancelledError:
                pass

        self.heartbeat_loop = asyncio.create_task(heartbeat_loop())

    async def stop_heartbeat(self) -> None:
        if self.heartbeat_loop:
            self.heartbeat_loop.cancel()
            await asyncio.gather(self.heartbeat_loop, return_exceptions=True)
            self.heartbeat_loop = None

    async def send_heartbeat(self) -> None:
        await self.send_payload(
            {
                "op": self.HEARTBEAT,
                "d": self.sequence,
            }
        )
        self.last_heartbeat = time.perf_counter()

    async def on_dispatch(self, dispatch: GatewayPayload) -> None:
        if dispatch["t"] == "READY":
            self.session_id = cast(dict[str, str], dispatch["d"])["session_id"]

        task = asyncio.create_task(self.handle_dispatch(dispatch))
        self.tasks.append(task)
        task.add_done_callback(lambda t: self.tasks.remove(t))
        task.add_done_callback(lambda t: t.result())
