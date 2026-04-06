

# from django.db import transaction
# from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError

# from apps.department.models import Department
# from apps.access.models import Permission, UserPermission, UserRole, Role
# from apps.common.constants import RoleCodes, HIDDEN_FROM_DEPARTMENT_ADMIN
# from apps.common.helpers.authz.role_helpers import has_role
# from uuid import UUID

# User = get_user_model()

# # Management roles are not tied to any system — skip allowed_systems check
# MANAGEMENT_ROLES = {
#     RoleCodes.PLATFORM_ADMIN,
#     RoleCodes.PLATFORM_VIEWER,
#     RoleCodes.DEPT_ADMIN,
#     RoleCodes.DEPT_VIEWER,
# }

# @transaction.atomic
# def create_user(
#     *,
#     actor,
#     username: str,
#     password: str,
#     email: str | None = None,
#     department_id: UUID | None = None,
#     role_ids: list[UUID] | None = None,
# ):
#     role_ids = role_ids or []

#     # --------------------------------------------------
#     # 1️⃣ Identify actor type
#     # --------------------------------------------------
#     is_superuser = actor.is_superuser
#     is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
#     is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)

#     if not is_superuser and not is_platform_admin and not is_dept_admin:
#         raise ValidationError("You do not have permission to create users.")

#     # --------------------------------------------------
#     # 2️⃣ Username uniqueness
#     # --------------------------------------------------
#     if User.objects.filter(username=username).exists():
#         raise ValidationError({"username": ["Username already exists."]})

#     # --------------------------------------------------
#     # 3️⃣ Resolve department
#     #    Superuser / Platform Admin → caller provides department (required)
#     #    Dept Admin                 → auto-set to actor's department
#     # --------------------------------------------------
#     if is_superuser or is_platform_admin:
#         if not department_id:
#             raise ValidationError({"department": ["Department is required."]})
#         try:
#             department = Department.objects.get(id=department_id)
#         except Department.DoesNotExist:
#             raise ValidationError({"department": ["Invalid department."]})
#     else:
#         department = actor.department

#     # --------------------------------------------------
#     # 4️⃣ Resolve roles by UUID
#     # --------------------------------------------------
#     if not role_ids:
#         raise ValidationError({"roles": ["At least one role is required."]})

#     roles = Role.objects.filter(id__in=role_ids)
#     found_role_ids = set(roles.values_list("id", flat=True))
#     missing_roles = set(role_ids) - found_role_ids

#     if missing_roles:
#         raise ValidationError({"roles": ["Some roles are invalid."]})

#     # --------------------------------------------------
#     # 5️⃣ Validate role scope per actor
#     #
#     #    Superuser      → any role allowed
#     #    Platform Admin → no platform.admin + dept allowed_systems
#     #    Dept Admin     → no hidden roles + dept allowed_systems
#     # --------------------------------------------------
#     allowed_systems = set(department.allowed_systems)

#     if is_platform_admin:
#         for role in roles:
#             if role.code == RoleCodes.PLATFORM_ADMIN:
#                 raise ValidationError(
#                     {"roles": ["You cannot assign the platform.admin role."]}
#                 )
#             system = role.code.split(".")[0]
#             if system not in allowed_systems:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' is not allowed for this department."]}
#                 )

#     elif is_dept_admin:
#         for role in roles:
#             if role.code in HIDDEN_FROM_DEPARTMENT_ADMIN:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' cannot be assigned by department admin."]}
#                 )
#             system = role.code.split(".")[0]
#             if system not in allowed_systems:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' is not allowed for this department."]}
#                 )

#     # --------------------------------------------------
#     # 6️⃣ Expand roles → policies → permissions
#     #    Role is a preset. We walk all the way down to
#     #    individual permissions — that is what gets saved.
#     # --------------------------------------------------
#     permissions = Permission.objects.filter(
#         permission_policies__policy__policy_roles__role__in=roles
#     ).distinct()

#     if not permissions.exists():
#         raise ValidationError(
#             {"roles": ["Selected roles have no permissions assigned. Contact your administrator."]}
#         )

#     # --------------------------------------------------
#     # 7️⃣ Create user
#     # --------------------------------------------------
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email or "",
#         department=department,
#         is_active=True,
#     )

#     # --------------------------------------------------
#     # 8️⃣ Store UserPermission — source of truth
#     #    All expanded from roles → source="role"
#     # --------------------------------------------------
#     UserPermission.objects.bulk_create([
#         UserPermission(
#             user=user,
#             permission=permission,
#             assigned_by=actor,
#             source=UserPermission.SOURCE_ROLE,
#         )
#         for permission in permissions
#     ])

#     # --------------------------------------------------
#     # 9️⃣ Store UserRole — for UI display and reporting only
#     # --------------------------------------------------
#     UserRole.objects.bulk_create([
#         UserRole(user=user, role=role, assigned_by=actor)
#         for role in roles
#     ])

#     return user


from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.department.models import Department
from apps.access.models import Permission, UserPermission, UserRole, Role
from apps.common.constants import RoleCodes, HIDDEN_FROM_DEPARTMENT_ADMIN, MANAGEMENT_ROLES
from apps.common.helpers.authz.role_helpers import has_role
from uuid import UUID

User = get_user_model()


@transaction.atomic
def create_user(
    *,
    actor,
    username: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    email: str | None = None,
    department_id: UUID | None = None,
    role_ids: list[UUID] | None = None,
):
    role_ids = role_ids or []

    # --------------------------------------------------
    # 1️⃣ Identify actor type
    # --------------------------------------------------
    is_superuser = actor.is_superuser
    is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
    is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)

    if not is_superuser and not is_platform_admin and not is_dept_admin:
        raise ValidationError("You do not have permission to create users.")

    # --------------------------------------------------
    # 2️⃣ Username uniqueness
    # --------------------------------------------------
    if User.objects.filter(username=username).exists():
        raise ValidationError({"username": ["Username already exists."]})

    # --------------------------------------------------
    # 3️⃣ Resolve department
    #    Superuser / Platform Admin → caller provides department (required)
    #    Dept Admin                 → auto-set to actor's department
    # --------------------------------------------------
    if is_superuser or is_platform_admin:
        if not department_id:
            raise ValidationError({"department": ["Department is required."]})
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise ValidationError({"department": ["Invalid department."]})
    else:
        department = actor.department

    # --------------------------------------------------
    # 4️⃣ Resolve roles by UUID
    # --------------------------------------------------
    if not role_ids:
        raise ValidationError({"roles": ["At least one role is required."]})

    roles = Role.objects.filter(id__in=role_ids)
    found_role_ids = set(roles.values_list("id", flat=True))
    missing_roles = set(role_ids) - found_role_ids

    if missing_roles:
        raise ValidationError({"roles": ["Some roles are invalid."]})

    # --------------------------------------------------
    # 5️⃣ Validate role scope per actor
    #
    #    Superuser      → any role allowed
    #    Platform Admin → no platform.admin + system roles must match dept
    #    Dept Admin     → no hidden roles + system roles must match dept
    #
    #    Management roles (dept.*, platform.*) are NOT system roles
    #    and are exempt from the allowed_systems check.
    # --------------------------------------------------
    allowed_systems = set(department.allowed_systems)

    if is_platform_admin:
        for role in roles:
            if role.code == RoleCodes.PLATFORM_ADMIN:
                raise ValidationError(
                    {"roles": ["You cannot assign the platform.admin role."]}
                )
            # Skip system check for management roles
            # if role.code in MANAGEMENT_ROLES:
            #     continue
            # system = role.code.split(".")[0]
            # if system not in allowed_systems:
            #     raise ValidationError(
            #         {"roles": [f"Role '{role.code}' is not allowed for this department."]}
            #     )

    elif is_dept_admin:
        for role in roles:
            if role.code in HIDDEN_FROM_DEPARTMENT_ADMIN:
                raise ValidationError(
                    {"roles": [f"Role '{role.code}' cannot be assigned by department admin."]}
                )
            # Skip system check for management roles
            if role.code in MANAGEMENT_ROLES:
                continue
            system = role.code.split(".")[0]
            if system not in allowed_systems:
                raise ValidationError(
                    {"roles": [f"Role '{role.code}' is not allowed for this department."]}
                )

    # --------------------------------------------------
    # 6️⃣ Expand roles → policies → permissions
    #    Role is a preset. We walk all the way down to
    #    individual permissions — that is what gets saved.
    # --------------------------------------------------
    permissions = Permission.objects.filter(
        permission_policies__policy__policy_roles__role__in=roles
    ).distinct()

    if not permissions.exists():
        raise ValidationError(
            {"roles": ["Selected roles have no permissions assigned. Contact your administrator."]}
        )

    # --------------------------------------------------
    # 7️⃣ Create user
    # --------------------------------------------------
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email or "",
        department=department,
        is_active=True,
        must_change_password=True,
    )

    # --------------------------------------------------
    # 8️⃣ Store UserPermission — source of truth
    #    All expanded from roles → source="role"
    # --------------------------------------------------
    UserPermission.objects.bulk_create([
        UserPermission(
            user=user,
            permission=permission,
            assigned_by=actor,
            source=UserPermission.SOURCE_ROLE,
        )
        for permission in permissions
    ])

    # --------------------------------------------------
    # 9️⃣ Store UserRole — for UI display and reporting only
    # --------------------------------------------------
    UserRole.objects.bulk_create([
        UserRole(user=user, role=role, assigned_by=actor)
        for role in roles
    ])

    return user








# # apps/identity/services/user/create.py

# from django.db import transaction
# from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError

# from apps.department.models import Department
# from apps.access.models import Policy, UserPolicy, UserRole, Role
# from apps.common.constants import RoleCodes, HIDDEN_FROM_IAM_ADMIN
# from apps.common.helpers.authz.role_helpers import has_role
# from uuid import UUID

# User = get_user_model()


# @transaction.atomic
# def create_user(
#     *,
#     actor,
#     username: str,
#     password: str,
#     email: str | None = None,
#     department_id: UUID | None = None,
#     role_ids: list[UUID] | None = None,
#     extra_policy_ids: list[UUID] | None = None,
# ):
#     role_ids = role_ids or []
#     extra_policy_ids = extra_policy_ids or []

#     # --------------------------------------------------
#     # 1️⃣ Identify actor type
#     # --------------------------------------------------
#     is_superuser = actor.is_superuser
#     is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
#     is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)

#     if not is_superuser and not is_platform_admin and not is_dept_admin:
#         raise ValidationError("You do not have permission to create users.")

#     # --------------------------------------------------
#     # 2️⃣ Username uniqueness
#     # --------------------------------------------------
#     if User.objects.filter(username=username).exists():
#         raise ValidationError({"username": ["Username already exists."]})

#     # --------------------------------------------------
#     # 3️⃣ Resolve department
#     #    Superuser / Platform Admin → caller provides department (required)
#     #    Dept Admin                 → auto-set to actor's department
#     # --------------------------------------------------
#     if is_superuser or is_platform_admin:
#         if not department_id:
#             raise ValidationError({"department": ["Department is required."]})
#         try:
#             department = Department.objects.get(id=department_id)
#         except Department.DoesNotExist:
#             raise ValidationError({"department": ["Invalid department."]})
#     else:
#         department = actor.department

#     # --------------------------------------------------
#     # 4️⃣ Resolve roles by UUID
#     # --------------------------------------------------
#     if not role_ids:
#         raise ValidationError({"roles": ["At least one role is required."]})

#     roles = Role.objects.filter(id__in=role_ids)
#     found_role_ids = set(roles.values_list("id", flat=True))
#     missing_roles = set(role_ids) - found_role_ids

#     if missing_roles:
#         raise ValidationError({"roles": ["Some roles are invalid."]})

#     # --------------------------------------------------
#     # 5️⃣ Validate role scope per actor
#     #
#     #    Superuser      → any role allowed
#     #    Platform Admin → any role except platform.admin
#     #    Dept Admin     → only non-hidden, only roles for dept's allowed systems
#     # --------------------------------------------------
#     if is_platform_admin:
#         for role in roles:
#             if role.code == RoleCodes.PLATFORM_ADMIN:
#                 raise ValidationError(
#                     {"roles": ["You cannot assign the platform.admin role."]}
#                 )

#     elif is_dept_admin:
#         allowed_systems = set(department.allowed_systems)
#         for role in roles:
#             if role.code in HIDDEN_FROM_IAM_ADMIN:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' cannot be assigned by department admin."]}
#                 )
#             system = role.code.split(".")[0]
#             if system not in allowed_systems:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' is not allowed for this department."]}
#                 )

#     # --------------------------------------------------
#     # 6️⃣ Expand roles → policies (always included, cannot be removed)
#     # --------------------------------------------------
#     role_policy_ids = set(
#         Policy.objects.filter(
#             policy_roles__role__in=roles
#         ).values_list("id", flat=True)
#     )

#     # --------------------------------------------------
#     # 7️⃣ Resolve extra policies
#     #    Superuser / Platform Admin → allowed, added on top of role policies
#     #    Dept Admin                 → not allowed
#     # --------------------------------------------------
#     extra_policy_id_set = set()

#     if extra_policy_ids:
#         if is_dept_admin:
#             raise ValidationError(
#                 {"extra_policies": ["Department admin cannot assign extra policies."]}
#             )

#         extra_policies = Policy.objects.filter(id__in=extra_policy_ids)
#         found_extra_ids = set(extra_policies.values_list("id", flat=True))
#         missing_extra = set(extra_policy_ids) - found_extra_ids

#         if missing_extra:
#             raise ValidationError({"extra_policies": ["Some policies are invalid."]})

#         extra_policy_id_set = found_extra_ids

#     # --------------------------------------------------
#     # 8️⃣ Merge final policies
#     #    Role policies (protected baseline) + extra policies (optional additions)
#     # --------------------------------------------------
#     final_policy_ids = role_policy_ids | extra_policy_id_set

#     if not final_policy_ids:
#         raise ValidationError(
#             {"roles": ["Selected roles have no policies assigned. Contact your administrator."]}
#         )

#     final_policies = Policy.objects.filter(id__in=final_policy_ids)

#     # --------------------------------------------------
#     # 9️⃣ Create user
#     # --------------------------------------------------
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email or "",
#         department=department,
#         is_active=True,
#     )

#     # --------------------------------------------------
#     # 🔟 Store UserPolicy — source of truth for permissions
#     # --------------------------------------------------
#     UserPolicy.objects.bulk_create([
#         UserPolicy(user=user, policy=policy, assigned_by=actor)
#         for policy in final_policies
#     ])

#     # --------------------------------------------------
#     # 1️⃣1️⃣ Store UserRole — for visibility and management rules
#     # --------------------------------------------------
#     UserRole.objects.bulk_create([
#         UserRole(user=user, role=role, assigned_by=actor)
#         for role in roles
#     ])

#     return user


# apps/identity/services/user/create.py

# from django.db import transaction
# from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError

# from apps.department.models import Department
# from apps.access.models import Policy, UserPolicy, UserRole, Role
# from apps.common.constants import RoleCodes, HIDDEN_FROM_IAM_ADMIN
# from apps.common.helpers.authz.role_helpers import has_role
# from uuid import UUID

# User = get_user_model()


# @transaction.atomic
# def create_user(
#     *,
#     actor,
#     username: str,
#     password: str,
#     email: str | None = None,
#     department_id: UUID | None = None,
#     role_ids: list[UUID] | None = None,
#     extra_policy_ids: list[UUID] | None = None,
# ):
#     role_ids = role_ids or []
#     extra_policy_ids = extra_policy_ids or []

#     # --------------------------------------------------
#     # 1️⃣ Identify actor type
#     # --------------------------------------------------
#     is_superuser = actor.is_superuser
#     is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
#     is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)

#     if not is_superuser and not is_platform_admin and not is_dept_admin:
#         raise ValidationError("You do not have permission to create users.")

#     # --------------------------------------------------
#     # 2️⃣ Username uniqueness
#     # --------------------------------------------------
#     if User.objects.filter(username=username).exists():
#         raise ValidationError({"username": ["Username already exists."]})

#     # --------------------------------------------------
#     # 3️⃣ Resolve department
#     #    Superuser / Platform Admin → caller provides department (required)
#     #    Dept Admin                 → auto-set to actor's department
#     # --------------------------------------------------
#     if is_superuser or is_platform_admin:
#         if not department_id:
#             raise ValidationError({"department": ["Department is required."]})
#         try:
#             department = Department.objects.get(id=department_id)
#         except Department.DoesNotExist:
#             raise ValidationError({"department": ["Invalid department."]})
#     else:
#         department = actor.department

#     # --------------------------------------------------
#     # 4️⃣ Resolve roles by UUID
#     # --------------------------------------------------
#     if not role_ids:
#         raise ValidationError({"roles": ["At least one role is required."]})

#     roles = Role.objects.filter(id__in=role_ids)
#     found_role_ids = set(roles.values_list("id", flat=True))
#     missing_roles = set(role_ids) - found_role_ids

#     if missing_roles:
#         raise ValidationError({"roles": ["Some roles are invalid."]})

#     # --------------------------------------------------
#     # 5️⃣ Validate role scope per actor
#     #
#     #    Superuser      → any role allowed
#     #    Platform Admin → no platform.admin + dept allowed_systems
#     #    Dept Admin     → no hidden roles + dept allowed_systems
#     # --------------------------------------------------
#     allowed_systems = set(department.allowed_systems)

#     if is_platform_admin:
#         for role in roles:
#             if role.code == RoleCodes.PLATFORM_ADMIN:
#                 raise ValidationError(
#                     {"roles": ["You cannot assign the platform.admin role."]}
#                 )
#             system = role.code.split(".")[0]
#             if system not in allowed_systems:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' is not allowed for this department."]}
#                 )

#     elif is_dept_admin:
#         for role in roles:
#             if role.code in HIDDEN_FROM_IAM_ADMIN:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' cannot be assigned by department admin."]}
#                 )
#             system = role.code.split(".")[0]
#             if system not in allowed_systems:
#                 raise ValidationError(
#                     {"roles": [f"Role '{role.code}' is not allowed for this department."]}
#                 )

#     # --------------------------------------------------
#     # 6️⃣ Expand roles → policies (protected baseline)
#     # --------------------------------------------------
#     role_policies = Policy.objects.filter(
#         policy_roles__role__in=roles
#     )
#     role_policy_ids = set(role_policies.values_list("id", flat=True))

#     # --------------------------------------------------
#     # 7️⃣ Resolve extra policies
#     #    Superuser      → any policy allowed
#     #    Platform Admin → allowed, scoped to department allowed_systems
#     #    Dept Admin     → blocked entirely
#     # --------------------------------------------------
#     extra_policy_id_set = set()

#     if extra_policy_ids:
#         if is_dept_admin:
#             raise ValidationError(
#                 {"extra_policies": ["Department admin cannot assign extra policies."]}
#             )

#         extra_policies = Policy.objects.filter(id__in=extra_policy_ids)
#         found_extra_ids = set(extra_policies.values_list("id", flat=True))
#         missing_extra = set(extra_policy_ids) - found_extra_ids

#         if missing_extra:
#             raise ValidationError({"extra_policies": ["Some policies are invalid."]})

#         if is_platform_admin:
#             for policy in extra_policies:
#                 system = policy.code.split(".")[0]
#                 if system not in allowed_systems:
#                     raise ValidationError(
#                         {"extra_policies": [f"Policy '{policy.code}' is not allowed for this department."]}
#                     )

#         extra_policy_id_set = found_extra_ids

#     # --------------------------------------------------
#     # 8️⃣ Merge final policies
#     # --------------------------------------------------
#     final_policy_ids = role_policy_ids | extra_policy_id_set

#     if not final_policy_ids:
#         raise ValidationError(
#             {"roles": ["Selected roles have no policies assigned. Contact your administrator."]}
#         )

#     # --------------------------------------------------
#     # 9️⃣ Create user
#     # --------------------------------------------------
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email or "",
#         department=department,
#         is_active=True,
#     )

#     # --------------------------------------------------
#     # 🔟 Store UserPolicy — source of truth for permissions
#     #    Role-expanded policies → source="role"
#     #    Manually added extras  → source="extra"
#     # --------------------------------------------------
#     role_policy_objects = Policy.objects.filter(id__in=role_policy_ids)
#     extra_policy_objects = Policy.objects.filter(id__in=extra_policy_id_set)

#     UserPolicy.objects.bulk_create([
#         UserPolicy(user=user, policy=policy, assigned_by=actor, source=UserPolicy.SOURCE_ROLE)
#         for policy in role_policy_objects
#     ] + [
#         UserPolicy(user=user, policy=policy, assigned_by=actor, source=UserPolicy.SOURCE_EXTRA)
#         for policy in extra_policy_objects
#     ])

#     # --------------------------------------------------
#     # 1️⃣1️⃣ Store UserRole — for visibility and management rules
#     # --------------------------------------------------
#     UserRole.objects.bulk_create([
#         UserRole(user=user, role=role, assigned_by=actor)
#         for role in roles
#     ])

#     return user
