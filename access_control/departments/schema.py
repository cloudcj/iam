from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Department:
    name: str
    label: str
    allowed_roles: Tuple[str, ...]
