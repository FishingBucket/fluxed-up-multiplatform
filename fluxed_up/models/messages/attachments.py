__all__ = ["Attachment"]

from datetime import datetime

from ...platform import Platform
from .files import File  # noqa # used for the documentation


class Attachment:
    """
    Represents an attachment in a returning message. The capabilities of this class depends on the platform.

    If you want to send a file instead, use the :class:`File` class.

    Attributes
    ----------
    filename : str
        The file name of the attachment.
    title : str | None
        The title of the attachment displayed by the client.
    description : str | None
        The alt text of the attachment.
    url : str | None
        The URL of the attachment content. This is the signed URL and carries expiration and other metadata.
        On Fluxer, when the attachment expires, this field is set to ``None``.
    expires : :class:`datetime` | None
        The time at which this attachment expires, or ``None`` if it never expires, or the platform is Discord.
    platform : :class:`Platform`
        The platform this attachment is for.
    """

    __slots__ = ("description", "expires", "filename", "platform", "title", "url")

    filename: str
    title: str | None
    description: str | None
    url: str | None
    expires: datetime | None
    platform: Platform
