__all__ = ["Guild", "GuildID"]

from typing import Protocol

from ..model import Model
from ..snowflake import Snowflake
from ..user import UserID


class GuildID(Snowflake):
    """
    A :class:`Snowflake` representing a guild ID.
    """


class Guild(Model, Protocol):
    """
    Represents a guild, community, server, etc., on a platform.

    .. traits::
        .. trait:: eq
            .. based-on:: ID
        .. trait:: repr
            .. based-on:: ID

    Attributes
    ----------
    id : :class:`GuildID`
        The ID of this Guild.
    name : str
        The name of this Guild.
    owner_id : :class:`UserID`
        The owner of this Guild.
    """

    id: GuildID
    name: str
    owner_id: UserID
