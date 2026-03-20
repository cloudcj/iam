from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Role:
    code: str
    name: str
    policies: Tuple[str, ...]
