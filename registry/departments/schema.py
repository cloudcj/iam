from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Department:
    code: str
    name: str
    allowed_systems: Tuple[str, ...]
