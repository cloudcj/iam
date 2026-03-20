from .inventory import INVENTORY_POLICIES
from .iam import IAM_POLICIES
from .global_policies import GLOBAL_POLICIES


# def all_permissions_for_system(system_name: str) -> tuple[str, ...]:
#     service = POLICIES_REGISTRY[system_name]
#     perms = []

#     for resource in service.resources.values():
#         for action in resource.actions.values():
#             perms.append(action.code)

#     return tuple(perms)


# def read_permissions_for_service(service_name: str) -> tuple[str, ...]:
#     service = POLICIES_REGISTRY[service_name]
#     perms = []

#     for resource in service.resources.values():
#         if "read" in resource.actions:
#             perms.append(resource.actions["read"].code)

#     return tuple(perms)


POLICIES_REGISTRY = {
    **INVENTORY_POLICIES,
    **IAM_POLICIES,
    **GLOBAL_POLICIES,
}
