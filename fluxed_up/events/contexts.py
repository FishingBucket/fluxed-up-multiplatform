__all__ = [
    "BaseContext",
    "OnEditContext",
    "OnGuildAvailable",
    "OnMessageContext",
    "OnReadyContext",
]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client.concrete_client import ConcreteClient
    from ..models.guilds.guilds import Guild
    from ..models.messages.messages import Message
    from ..models.users import User, UserProfile
    from ..platform import Platform


class BaseContext:
    platform: Platform
    client: ConcreteClient


class OnReadyContext(BaseContext):
    session_id: str
    user: User
    user_profile: UserProfile
    guilds: list[Guild]


class OnMessageContext(BaseContext):
    message: Message


class OnEditContext(BaseContext):
    message: Message


class OnGuildAvailable(BaseContext):
    guild: Guild
