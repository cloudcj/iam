from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.department.models import Department
from apps.access.models import Role, UserRole, Permission, UserPermission
from apps.common.constants import RoleCodes, HIDDEN_FROM_DEPARTMENT_ADMIN, MANAGEMENT_ROLES
from apps.common.helpers.authz.role_helpers import has_role
from apps.authz.services.authorization_service import AuthorizationService

User = get_user_model()

@transaction.atomic
def update_user(*, actor, target, username=None, first_name, last_name, email, is_active, department_id, role_ids, permission_ids=None):
    is_superuser = actor.is_superuser
    is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
    is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)

    # Resolve department
    if is_superuser or is_platform_admin:
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise ValidationError({"department": ["Invalid department."]})
    else:
        department = actor.department

    # Resolve roles
    roles = Role.objects.filter(id__in=role_ids)
    found_role_ids = set(roles.values_list("id", flat=True))
    missing = set(role_ids) - found_role_ids
    if missing:
        raise ValidationError({"roles": ["Some roles are invalid."]})

    # Validate role scope
    allowed_systems = set(department.allowed_systems)

    if is_platform_admin:
        for role in roles:
            if role.code == RoleCodes.PLATFORM_ADMIN:
                raise ValidationError({"roles": ["You cannot assign the platform.admin role."]})
            if role.code in MANAGEMENT_ROLES:
                continue
            system = role.code.split(".")[0]
            if system not in allowed_systems:
                raise ValidationError({"roles": [f"Role '{role.code}' is not allowed for this department."]})

    elif is_dept_admin:
        for role in roles:
            if role.code in HIDDEN_FROM_DEPARTMENT_ADMIN:
                raise ValidationError({"roles": [f"Role '{role.code}' cannot be assigned by department admin."]})
            if role.code in MANAGEMENT_ROLES:
                continue
            system = role.code.split(".")[0]
            if system not in allowed_systems:
                raise ValidationError({"roles": [f"Role '{role.code}' is not allowed for this department."]})

    # Update basic info
    update_fields = ["first_name", "last_name", "email", "department"]
    target.first_name = first_name
    target.last_name = last_name
    target.email = email
    target.department = department
    if username:
        target.username = username
        update_fields.append("username")
    target.save(update_fields=update_fields)

    # Replace roles
    UserRole.objects.filter(user=target).delete()
    UserRole.objects.bulk_create([
        UserRole(user=target, role=role, assigned_by=actor)
        for role in roles
    ])

    if is_superuser:
        # Full override — delete ALL permissions, re-insert only what superuser checked
        # Roles are just presets/UI — superuser's checked permissions are the source of truth
        UserPermission.objects.filter(user=target).delete()
        if permission_ids:
            UserPermission.objects.bulk_create([
                UserPermission(
                    user=target,
                    permission_id=perm_id,
                    assigned_by=actor,
                    source=UserPermission.SOURCE_DIRECT,
                )
                for perm_id in set(permission_ids)
            ], ignore_conflicts=True)

    elif is_platform_admin:
        # Re-derive source=role from roles, replace source=direct with checked permissions
        role_permissions = set(
            Permission.objects.filter(
                permission_policies__policy__policy_roles__role__in=roles
            ).values_list("id", flat=True)
        )
        UserPermission.objects.filter(user=target, source=UserPermission.SOURCE_ROLE).delete()
        UserPermission.objects.bulk_create([
            UserPermission(
                user=target,
                permission_id=perm_id,
                assigned_by=actor,
                source=UserPermission.SOURCE_ROLE,
            )
            for perm_id in role_permissions
        ], ignore_conflicts=True)

        UserPermission.objects.filter(user=target, source=UserPermission.SOURCE_DIRECT).delete()
        if permission_ids:
            UserPermission.objects.bulk_create([
                UserPermission(
                    user=target,
                    permission_id=perm_id,
                    assigned_by=actor,
                    source=UserPermission.SOURCE_DIRECT,
                )
                for perm_id in set(permission_ids)
            ], ignore_conflicts=True)

    else:
        # Dept admin — re-derive source=role only, source=direct untouched
        role_permissions = set(
            Permission.objects.filter(
                permission_policies__policy__policy_roles__role__in=roles
            ).values_list("id", flat=True)
        )
        UserPermission.objects.filter(user=target, source=UserPermission.SOURCE_ROLE).delete()
        UserPermission.objects.bulk_create([
            UserPermission(
                user=target,
                permission_id=perm_id,
                assigned_by=actor,
                source=UserPermission.SOURCE_ROLE,
            )
            for perm_id in role_permissions
        ], ignore_conflicts=True)
    
    # Invalidate permission cache so next request reflects updated permissions
    AuthorizationService.invalidate_cache(target.id)


    return target
