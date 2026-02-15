# permissions/models.py
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Action:
    name: str
    code: str

@dataclass(frozen=True)
class Resource:
    name: str
    label: str
    actions: Dict[str, Action]

@dataclass(frozen=True)
class System:
    name: str
    label: str
    resources: Dict[str, Resource]
