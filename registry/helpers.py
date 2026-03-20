
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

# helpers.py
def all_permissions_for_service(service) -> tuple[str, ...]:
    perms = []

    for resource in service.resources.values():
        for action in resource.actions.values():
            perms.append(action.code)

    return tuple(perms)


def read_permissions_for_service(service) -> tuple[str, ...]:
    perms = []

    for resource in service.resources.values():
        if "read" in resource.actions:
            perms.append(resource.actions["read"].code)

    return tuple(perms)
