__all__ = ["File"]

from ...platform import Platform


class File:
    """
    Represents a file to be sent with a message. You want to use this for requests.

    Attributes
    ----------
    filename : str
        The file name of the file to be sent.
    platform : :class:`Platform`
        The platform that this file is for.
    """

    __slots__ = ("filename", "platform")

    filename: str
    platform: Platform

    def __init__(
        self,
        filename: str,
        platform: Platform = Platform.Auto,
    ) -> None:
        self.filename = filename
        self.platform = platform
