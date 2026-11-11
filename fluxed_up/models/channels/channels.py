__all__ = ["ChannelID"]

from enum import Enum

from ..guilds import GuildID
from ..snowflake import Snowflake


class ChannelID(Snowflake):
    """
    A :class:`Snowflake` representing a channel ID.
    """


class ChannelType(Enum):
    """
    The :class:`Channel` type. This enum contains platform-specific members.

    .. container:: todo
        Finish :ref:`fluxed_up.utils.multiplatform.DependentEnum` and then migrate this enum to that class.
        This raw :class:`Enum` is only a temporary solution.
    """

    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    """Discord-specific"""
    GUILD_DIRECTORY = 14
    """Discord-specific"""
    GUILD_FORUM = 15
    GUILD_MEDIA = 16
    """Fluxer-specific, but in development on Discord. Use with care."""
    GUILD_LINK = 998
    """Fluxer-specific"""
    DM_PERSONAL_NOTES = 999
    """Fluxer-specific"""


class Channel:
    """
    Represents a channel or message-able room on a platform.

    .. traits::
        .. trait:: eq
            .. based-on:: ID

    Attributes
    ----------
    id : :class:`ChannelID`
        The ID of this Channel.
    type : :class:`ChannelType`
        The type of this Channel.
    guild_id : :class:`GuildID` | None
        The guild ID that this Channel belongs to. If it is ``None``, then the channel doesn't belong in a guild,
        and is likely a DM channel or a group DM.
    name : str
        The name of this Channel.
    description : str
        The description, or topic, of this Channel.
    position : int
        The position of this Channel in the channel list.
    parent_id : :class:`ChannelID` | None
        The parent category of this Channel, if any. If this Channel is a thread, then this value is the parent channel.
    """

    __slots__ = (
        "description",
        "guild_id",
        "id",
        "name",
        "parent_id",
        "position",
        "type",
    )

    id: ChannelID
    type: ChannelType
    guild_id: GuildID | None
    name: str
    description: str
    position: int
    parent_id: ChannelID | None
