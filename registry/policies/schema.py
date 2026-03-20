from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Policy:
    code: str
    name: str
    system: str
    resource: str
    permissions: tuple[str, ...]
    visible_in_ui: bool = True

