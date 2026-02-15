from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Role:
    code: str
    label: str
    policies: Tuple[str, ...]
