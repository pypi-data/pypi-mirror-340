from typing import Mapping, Sequence

type Jsonable = Mapping[str, "Jsonable"] | Sequence[
    "Jsonable"
] | str | int | float | bool | None
