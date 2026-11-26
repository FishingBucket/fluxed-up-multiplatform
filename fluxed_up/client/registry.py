__all__ = ["BaseRegistry"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from .client_ghost import ClientGhost  # noqa # used in docs


class BaseRegistry[T](ABC):
    """
    Abstract base class for all registries to hook into a :class:`Client`.

    Attributes
    ----------
    registered : set[int]
        A set of :class:`ClientGhost` IDs that have been registered.
    registrations: list[T]
        A list of the items registered into this registry.
    """

    registered: set[int]
    registrations: list[T]

    def __init__(self) -> None:
        self.registrations = []
        self.registered = set()

    def hook_into(self, client: Client) -> None:
        """
        Registers everything inside this registry into a :class:`Client`.

        This function is idempotent for a :class:`Client`.

        Parameters
        ----------
        client : :class:`Client`
            The client to hook behavior into.
        """
        if id(client) not in self.registered:
            self._hook_into(client)

    def register(self, item: T) -> None:
        """
        Registers an item into this registry.

        Parameters
        ----------
        item : T
            The item to register.
        """
        self.registrations.append(item)

    @abstractmethod
    def _hook_into(self, client: Client) -> None:
        raise NotImplementedError
