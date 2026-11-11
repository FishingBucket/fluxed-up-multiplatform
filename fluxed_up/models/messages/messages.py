from ...platform import Platform
from ..channels import ChannelID
from ..snowflake import Snowflake
from ..user import User
from .attachments import Attachment
from .embeds import Embed

__all__ = ["Message", "MessageID", "MessageRef"]


class MessageID(Snowflake):
    """
    A :class:`Snowflake` representing a message's ID, but this cannot pinpoint a specific message.
    To pinpoint a specific message for fetch and other things, use :class:`MessageRef`.
    """


class MessageRef:
    """
    Unique identifier for a specific :class:`Message`.

    This class combines the message's ID (:class:`MessageID`) and the channel ID (:class:`ChannelID`)
    to create a record that can be used in fetch methods and operations.

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
        Platform.raise_if_unmatched(message.platform, channel.platform)

        self.message = message
        self.channel = channel

    def __repr__(self) -> str:
        return f"MessageID({self.message!r}, {self.channel!r})"

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


class Message:
    """
    Represents a message sent on a platform.

    .. traits::
        .. trait:: eq
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

    __slots__ = ("attachments", "author", "channel_id", "content", "embeds", "id")

    id: MessageID
    channel_id: ChannelID
    author: User
    content: str
    embeds: list[Embed]
    attachments: list[Attachment]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Message) and self.id == other.id and self.channel_id == other.channel_id

    @property
    def ref(self) -> MessageRef:
        """
        Returns
        -------
        :class:`MessageRef`
            A reference to this Message that can be used in fetch operations.
        """
        return MessageRef(self.id, self.channel_id)
