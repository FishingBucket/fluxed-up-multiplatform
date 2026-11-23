__all__ = ["JSON"]

from collections.abc import Mapping, Sequence

type JSON = Mapping[str, JSON] | Sequence[JSON] | str | int | float | bool | None
