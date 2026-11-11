from collections.abc import Hashable
from enum import EnumType
from enum import auto as default_auto
from typing import cast


class auto[K = str, V = int](default_auto):
    """
    A specific version of :class:`enum.auto` for :class:`DependentEnum`.

    .. traits::
        .. trait:: repr
            .. type:: construction
        .. trait:: index
            Gets the value of the internal ``items``.

    Attributes
    ----------
    items : dict[K, V]
        The items that this enum member will take on for a dependency value.

    Parameters
    ----------
    items : dict[K, V], optional
        The items that this enum member will take on for a dependency value.
        If this value is supplied, then kwargs cannot be supplied.
    kwargs : V
        Simple case to supply the ``items`` parameter when the type of ``K`` is :class:`str`.

    See Also
    --------
    :class:`DependentEnum`
    """

    __slots__ = ("items",)

    items: dict[K, V]

    def __init__(self, items: dict[K, V] | None = None, /, **kwargs: V) -> None:
        if items and kwargs:
            raise TypeError("Cannot specify both an items dict and kwargs.")

        if items:
            self.items = items
        else:
            self.items = cast(dict[K, V], kwargs)

    def __repr__(self) -> str:
        return f"auto({self.items!r})"

    def __getitem__(self, key: K) -> V:
        return self.items[key]


# TODO: what the fuck is this.
class DependentEnum[DependencyType: Hashable, DependencyValue = int](EnumType):
    """
    A sibling of :class:`Enum` specifically for values that change values depending on some other external value.

    Members uses :class:`auto` (this is not :class:`enum.auto`) to specify dependency-aware values.

    All possible dependency values are specified with the class attribute :attr:`__dep_values__`.

    .. traits::
        .. trait:: repr
            .. type:: construction

    Examples
    --------
    >>> from typing import Literal
    >>> class AlternateMath(DependentEnum[Literal["Standard", "Alternate"]]):
    ...     __dep_values__ = {"Standard", "Alternate"}
    ...
    ...     NINE_PLUS_TEN = auto(Standard=19, Alternate=21)
    ...     ONE_PLUS_ONE = auto(Standard=2, Alternate=1)
    >>> AlternateMath.NINE_PLUS_TEN
    AlternateMath.NINE_PLUS_TEN
    >>> AlternateMath(1, "Alternate")
    AlternateMath.ONE_PLUS_ONE
    >>> AlternateMath.NINE_PLUS_TEN.value["Standard"]
    19
    """
