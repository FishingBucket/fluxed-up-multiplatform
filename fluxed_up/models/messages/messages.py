from typing import TYPE_CHECKING, Protocol

from ...utils.metaprog import require_permissions
from ..model import Model
from ..permissions import Permissions
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from ...exceptions import MissingPermissions  # noqa # used in docstring
    from ..users import User
    from .attachments import Attachment
    from .embeds import Embed
    from .files import File
    from ..channels import ChannelID


__all__ = ["Message", "MessageID", "MessageRef"]


class MessageID(Snowflake):
    """
    A :class:`Snowflake` representing a message's ID, but this cannot pinpoint a specific message.
    To pinpoint a specific message for get and other things, use :class:`MessageRef`.
    """


class MessageRef:
    """
    Unique identifier for a specific :class:`Message`.

    This class combines the message's ID (:class:`MessageID`) and the channel ID (:class:`ChannelID`)
    to create a record that can be used in get methods and operations.

    Like :class:`Snowflake`, this class can be hashed, compared, and used as dictionary keys.

    .. traits::
        .. trait:: eq
            .. type:: total
            .. based-on:: message ID, channel ID
        .. trait:: hash
            .. based-on:: message ID, channel ID
        .. trait:: repr
            .. type:: construction
        .. trait:: str
            .. based-on:: message ID, channel ID
            The string representation is in the form of ``<channel ID>/<message ID>``.

    Attributes
    ----------
    message : :class:`MessageID`
        The message ID of this :class:`Message`.
    channel : :class:`ChannelID`
        The channel ID of this :class:`Message`.

    Parameters
    ----------
    message : :class:`MessageID`
        The message ID of this :class:`Message`.
    channel : :class:`ChannelID`
        The channel ID of this :class:`Message`.
    """

    __slots__ = ("channel", "message")

    message: MessageID
    channel: ChannelID

    def __init__(self, message: MessageID, channel: ChannelID) -> None:
        self.message = message
        self.channel = channel

    def __repr__(self) -> str:
        return f"MessageRef({self.message!r}, {self.channel!r})"

    def __str__(self) -> str:
        return f"{self.channel}/{self.message}"

    def __hash__(self) -> int:
        return hash((self.channel, self.message))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, MessageRef)
            and self.channel == other.channel
            and self.message == other.message
        )

    @property
    def timestamp(self) -> float:
        """
        Returns
        -------
        float
            The timestamp in seconds at which this :class:`Message` was sent.
        """
        return self.message.timestamp


class Message(Model, Protocol):
    """
    Represents a message sent on a platform.

    .. traits::
        .. trait:: eq
            .. based-on:: message ID, channel ID
        .. trait:: repr
            .. based-on:: message ID, channel ID

    Attributes
    ----------
    id : :class:`MessageID`
        The raw message ID of this Message.
    channel_id : :class:`ChannelID`
        The channel ID that this Message belongs to. This is required to pinpoint a specific message.
    content : str
        The content of this message. This may be an empty string.
    author : :class:`User`
        The user that sent this Message.
    embeds : list[:class:`Embed`]
        A list of :class:`Embed` objects that this Message has.
    attachments : list[:class:`Attachment`]
        A list of :class:`Attachment` objects that this Message has.
    """

    id: MessageID
    channel_id: ChannelID
    author: User
    content: str
    embeds: list[Embed]
    attachments: list[Attachment]

    @property
    def ref(self) -> MessageRef:
        """
        Returns
        -------
        :class:`MessageRef`
            A reference to this Message that can be used in get operations.
        """
        return MessageRef(self.id, self.channel_id)

    @require_permissions(Permissions.MANAGE_MESSAGES)
    async def delete(self, *, audit_reason: str | None = None) -> None:
        """
        Deletes this Message.

        |coro|

        |perms| :enum:mem:`Permissions.MANAGE_MESSAGES`

        Other Parameters
        ----------------
        audit_reason : str, optional
            The reason for deleting this Message.
        """
        raise NotImplementedError

    @require_permissions(Permissions.PIN_MESSAGES)
    async def pin(self, *, audit_reason: str | None = None) -> None:
        """
        Pins this Message to the channel.

        |coro|

        |perms| :enum:mem:`Permissions.PIN_MESSAGES`

        Other Parameters
        ----------------
        audit_reason : str, optional
            The reason for pinning this Message.
        """
        raise NotImplementedError

    @require_permissions(Permissions.PIN_MESSAGES)
    async def unpin(self, *, audit_reason: str | None = None) -> None:
        """
        Unpins this Message from the channel.

        |coro|

        |perms| :enum:`Permissions.PIN_MESSAGES`

        Other Parameters
        ----------------
        audit_reason : str, optional
            The reason for unpinning this Message.
        """
        raise NotImplementedError

    @require_permissions(Permissions.MANAGE_MESSAGES)
    async def suppress_embeds(self, *, audit_reason: str | None = None) -> None:
        """
        Suppresses the embeds on this Message.

        |coro|

        |perms| :enum:mem:`Permissions.MANAGE_MESSAGES`

        Other Parameters
        ----------------
        audit_reason : str, optional
            The reason for suppressing the embeds on this Message.
        """
        raise NotImplementedError


class MyMessage(Message, Protocol):
    """
    Represents a message sent on a platform by the current client. This class is a :class:`Message`.

    .. traits::
        .. trait:: eq
            .. based-on:: message ID, channel ID
        .. trait:: repr
            .. based-on:: message ID, channel ID
    """

    @require_permissions(Permissions.none())
    async def edit(
        self,
        content: str | None = None,
        *,
        embeds: list[Embed] | None = None,
        files: list[File] | None = None,
    ) -> None:
        """
        Edits this Message. If a parameter is ``None``, then that field is not edited.

        |coro|

        Parameters
        ----------
        content : str, optional
            The content of the new Message.

        Other Parameters
        ----------------
        embeds : list[:class:`Embed`], default=[]
            The embeds of the new Message.
        files : list[:class:`File`], default=[]
            The files of the new Message.
        """
        raise NotImplementedError

    @require_permissions(Permissions.none())
    async def delete(self, *, audit_reason: str | None = None) -> None:
        """
        Deletes this Message. Because this is your own message, no permissions are needed.

        |coro|

        Other Parameters
        ----------------
        audit_reason : str, optional
            The reason for deleting this Message.
        """
        raise NotImplementedError
