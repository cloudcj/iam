from access_control.services import PERMISSION_REGISTRY
from apps.access.models import Permission

# def generate_permission_description(service, resource, action):
#     return f"{action.name.title()} {resource.label}"



# def seed_permissions():
#     for service in PERMISSION_REGISTRY.values():
#         for resource in service.resources.values():
#             for action in resource.actions.values():
#                 Permission.objects.update_or_create(
#                     code=action.code,
#                     defaults={
#                         "description": f"{action.name.title()} {resource.label}"
#                     }
#                 )

def seed_permissions():
    for system in PERMISSION_REGISTRY.values():
        for resource in system.resources.values():
            for action in resource.actions.values():
                Permission.objects.update_or_create(
                    code=action.code,
                    defaults={
                        "system": system.name,       # ← from Service
                        "resource": resource.name,    # ← from Resource
                        "action": action.name,   
                        "description": (
                            f"{system.label} – "
                            f"{resource.label} – "
                            f"{action.name.title()}"
                        )
                    },
                )

# description format

# <System Label> – <Resource Label> – <Action Title>
