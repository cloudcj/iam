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

def make_system(name: str, label: str, resources: dict) -> System:
    built_resources = {}
    for res_name, (res_label, action_names) in resources.items():
        built_resources[res_name] = Resource(
            name=res_name,
            label=res_label,
            actions={
                action: Action(
                    name=action,
                    code=f"{name}.{res_name}.{action}",
                )
                for action in action_names
            },
        )
    return System(name=name, label=label, resources=built_resources)