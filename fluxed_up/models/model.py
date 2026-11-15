__all__ = ["Model"]

from typing import Protocol, runtime_checkable

from ..platform import Platform


@runtime_checkable
class Model(Protocol):
    """
    The basis of a platform model.
    """

    platform: Platform

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
