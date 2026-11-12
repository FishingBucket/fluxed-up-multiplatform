__all__ = ["File"]

from io import BytesIO
from typing import Protocol

from ...platform import Platform
from ..model import Model


class File(Model, Protocol):
    """
    Represents a file to be sent with a message. You want to use this for requests.

    Attributes
    ----------
    filename : str
        The file name of the File to be sent.
    platform : :class:`Platform`
        The platform that this File is for.
    data : bytes
        The data that this File contains.
    """

    filename: str
    platform: Platform
    data: bytes

    def __init__(
        self,
        filename: str,
        fp: BytesIO | bytes,
        platform: Platform = Platform.Auto,
    ) -> None:
        ...
