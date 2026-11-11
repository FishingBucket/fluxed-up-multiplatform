__all__ = ["Guild", "GuildID"]

from ..snowflake import Snowflake
from ..user import UserID


class GuildID(Snowflake):
    """
    A :class:`Snowflake` representing a guild ID.
    """


class Guild:
    """
    Represents a guild, community, server, etc., on a platform.

    .. traits::
        .. trait:: eq
            .. based-on: ID

    Attributes
    ----------
    id : :class:`GuildID`
        The ID of this Guild.
    name : str
        The name of this Guild.
    owner_id : :class:`UserID`
    """

    __slots__ = ("id", "name", "owner_id")

    id: GuildID
    name: str
    owner_id: UserID
