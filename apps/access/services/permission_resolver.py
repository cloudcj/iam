# def resolve_user_effective_permissions(user):
#     """
#     Resolve a user's assigned roles into effective permissions.

#     Returns:
#         roles: list[str]
#         permissions: list[str]
#     """
#     roles = set()
#     permissions = set()

#     user_roles = (
#         user.user_roles
#         .select_related("role")
#         .prefetch_related("role__permissions")
#     )

#     for user_role in user_roles:
#         role = user_role.role
#         roles.add(role.name)
#         permissions.update(
#             role.permissions.values_list("code", flat=True)
#         )

#     return list(roles), list(permissions)

from apps.authz.services.authorization_service import AuthorizationService


def resolve_user_effective_permissions(user):
    """
    Resolve a user's roles (display) and effective permissions (via AuthorizationService).

    Returns:
        roles: list[str]       — from UserRole (display only)
        permissions: list[str] — from UserPolicy via AuthorizationService (auth source of truth)
    """
    roles = list(
        user.user_roles
        .select_related("role")
        .values_list("role__name", flat=True)
    )

    permissions = list(AuthorizationService.get_user_permission_codes(user))

    return roles, permissions