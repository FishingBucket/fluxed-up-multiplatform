__all__ = ["Member"]

from typing import Protocol

from ..model import Model
from ..users import UserID
from .guilds import GuildID


class Member(Model, Protocol):
    """
    Represents a member of a guild for a platform.

    Attributes
    ----------
    id : :class:`UserID`
        The ID of the user.
    guild_id : :class:`GuildID`
        The ID of the guild that this member belongs to.
    """

    id: UserID
    guild_id: GuildID
