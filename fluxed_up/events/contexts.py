__all__ = ["OnEditContext", "OnGuildAvailable", "OnMessageContext", "OnReadyContext"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.guilds.guilds import Guild
    from ..models.messages.messages import Message
    from ..models.users import User, UserProfile


class OnReadyContext:
    session_id: str
    user: User
    user_profile: UserProfile
    guilds: list[Guild]


class OnMessageContext:
    message: Message


class OnEditContext:
    message: Message


class OnGuildAvailable:
    guild: Guild
