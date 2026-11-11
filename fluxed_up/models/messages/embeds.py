__all__ = ["Embed"]


from datetime import UTC, datetime

from ...platform import Platform
from ...utils import Color


class Embed:
    """
    Represents an embed in a message. The capabilities of this class depends on the platform.

    Attributes
    ----------
    title : str
        The title of the Embed.
    description : str
        The description of the Embed.
    url : str | None
        The url of the Embed.
        On Discord, when multiple Embeds are sent with the same URL, only one of them will be chosen.
    timestamp : :class:`datetime` | None
        The timestamp of the Embed.
    color : :class:`Color` | None
        The color of the Embed.
    platform: :class:`Platform`
        The platform that this embed is for.

    Parameters
    ----------
    title : str, default: ""
        The title of the Embed.
    description : str, default: ""
        The description of the Embed.
    platform : :class:`Platform`, default: :enum:mem:`Platform.Auto`
        The platform that this embed is for.

    Other Parameters
    ----------------
    url : str, optional
        The url of the Embed. Optional.
    timestamp : :class:`datetime` | float, optional
        The timestamp of the Embed. Optional. If the input is :class:`float`, it will be treated as seconds since epoch.
    color : :class:`Color`, optional
        The color of the Embed as a :class:`Color`. Optional.
    """

    __slots__ = ("color", "description", "platform", "timestamp", "title", "url")

    title: str
    description: str
    url: str | None
    timestamp: datetime | None
    color: Color | None
    platform: Platform

    def __init__(
        self,
        title: str = "",
        description: str = "",
        platform: Platform = Platform.Auto,
        *,
        url: str | None = None,
        timestamp: datetime | float | None = None,
        color: Color | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = (
            timestamp
            if isinstance(timestamp, datetime)
            else datetime.fromtimestamp(timestamp, UTC)
            if timestamp is not None
            else None
        )
        self.color = color
        self.platform = platform
