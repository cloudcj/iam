# # apps/access/services/role_service.py

# from django.db import transaction
# from django.core.exceptions import ValidationError

# from apps.access.models import Role, Permission, RolePermission
# from apps.audit.services.audit_logger import log_event


# @transaction.atomic
# def create_role(*, actor, name, permission_codes):
#     if not actor.is_superuser:
#         raise ValidationError("Only superusers can create roles")

#     role = Role.objects.create(name=name)

#     permissions = Permission.objects.filter(code__in=permission_codes)

#     RolePermission.objects.bulk_create([
#         RolePermission(role=role, permission=p)
#         for p in permissions
#     ])

#     log_event(
#         action="ROLE_CREATED",
#         user=actor,
#         metadata={
#             "role": name,
#             "permissions": permission_codes,
#         },
#     )

#     return role


# # Functions that belong in role_service

# # create_role
# # update_role
# # delete_role
# # add_permission_to_role
# # remove_permission_from_role
# # set_role_permissions