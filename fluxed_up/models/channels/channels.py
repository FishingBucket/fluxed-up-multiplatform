__all__ = ["Channel", "ChannelID", "ChannelType"]

from enum import Enum
from typing import TYPE_CHECKING, Protocol

from ...utils.metaprog import require_permissions
from ..model import Model
from ..permissions import Permissions
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from ...exceptions import MissingPermissions, ResourceNotFound  # noqa # used in docstring
    from ..guilds import GuildID
    from ..messages.embeds import Embed
    from ..messages.files import File
    from ..messages.messages import Message, MessageID


class ChannelID(Snowflake):
    """
    A :class:`Snowflake` representing a channel ID.
    """


class ChannelType(Enum):
    """
    A :class:`Channel` type. This enum contains platform-specific members.

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
    CHANNEL_OBFUSCATED = 17
    """Discord-specific"""
    GUILD_LINK = 998
    """Fluxer-specific"""
    DM_PERSONAL_NOTES = 999
    """Fluxer-specific"""


class Channel(Model, Protocol):
    """
    Represents a channel or message-able room on a platform.

    .. traits::
        .. trait:: eq
            .. based-on:: ID
        .. trait:: repr
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

    id: ChannelID
    type: ChannelType
    guild_id: GuildID | None
    name: str
    description: str
    position: int
    parent_id: ChannelID | None

    def __eq__(self, other: object | Channel) -> bool:
        return self.id == other.id  # type: ignore[union-attr]

    def __repr__(self) -> str:
        return f"Channel({self.id!r})"

    @require_permissions(Permissions.VIEW_CHANNEL | Permissions.SEND_MESSAGES)
    async def send_message(
        self,
        content: str,
        *,
        embeds: list[Embed] | None = None,
        files: list[File] | None = None,
    ) -> Message:
        """
        Sends a message to this Channel.

        |coro|

        |perms| :enum:mem:`Permissions.VIEW_CHANNEL` | :enum:mem:`Permissions.SEND_MESSAGES`

        Parameters
        ----------
        content : str
            The content of the message to send.
        embeds : list[:class:`Embed`], default=[]
            The list of embeds to send.
        files : list[:class:`File`], default=[]
            The list of files to attach.

        Returns
        -------
        :class:`Message`
            The message that was sent.
        """
        raise NotImplementedError

    @require_permissions(Permissions.VIEW_CHANNEL)
    async def get_message(self, message_id: MessageID) -> Message:
        """
        Gets a :class:`Message` from this Channel.

        |coro|

        |perms| :enum:mem:`Permissions.VIEW_CHANNEL`

        Parameters
        ----------
        message_id : :class:`MessageID`
            The ID of the message to get.

        Returns
        -------
        :class:`Message`
            The obtained message.

        Raises
        ------
        :exc:`ResourceNotFound`
            The client could not find the specified message.
        """
        raise NotImplementedError
