__all__ = ["EventRegistry"]

from collections.abc import Awaitable, Callable

from ..client.registry import BaseRegistry
from ..utils.metaprog import APIFunc
from .contexts import OnEditContext, OnGuildAvailable, OnMessageContext, OnReadyContext

type EventCallback[**P] = APIFunc[P, Awaitable[None]] | Callable[P, Awaitable[None]]


class EventRegistry(BaseRegistry[EventCallback[...]]):  # type: ignore[explicit-any]
    """
    A registry for events.
    """

    def on_ready[CB: EventCallback[[OnReadyContext]]](self, cb: CB) -> CB:
        """
        Registers a callback to be called when the client is online and ready.
        """
        self.register(cb)
        return cb

    def on_message[CB: EventCallback[[OnMessageContext]]](self, cb: CB) -> CB:
        """
        Registers a callback to be called when the client receives a message.
        """
        self.register(cb)
        return cb

    def on_edit[CB: EventCallback[[OnEditContext]]](self, cb: CB) -> CB:
        """
        Registers a callback to be called when a message is edited.
        """
        self.register(cb)
        return cb

    def on_guild_available[CB: EventCallback[[OnGuildAvailable]]](self, cb: CB) -> CB:
        """
        Registers a callback to be called when a guild is made available to the client.
        """
        self.register(cb)
        return cb
