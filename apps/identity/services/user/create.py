# apps/identity/services/user/create.py


from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.department.models import Department
from apps.access.models import Policy, UserPolicy, UserRole, Role

User = get_user_model()


from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.department.models import Department
from apps.access.models import Policy, UserPolicy, UserRole, Role
from uuid import UUID

User = get_user_model()

@transaction.atomic
def create_user(
    *,
    actor,
    username: str,
    password: str,
    department_id: UUID | None = None,
    role_ids: list[UUID] | None = None,
    policy_ids: list[UUID] | None = None,
    email: str | None = None,
):
    role_ids = role_ids or []
    policy_ids = policy_ids or []

    # --------------------------------------------------
    # 1️⃣ Authority Check
    # --------------------------------------------------
    if not actor.is_superuser and not actor.has_permission("iam.user.create"):
        raise ValidationError("You do not have permission to create users.")

    if User.objects.filter(username=username).exists():
        raise ValidationError({"username": ["Username already exists."]})

    # --------------------------------------------------
    # 2️⃣ Resolve Department
    # --------------------------------------------------
    if actor.is_superuser:
        if not department_id:
            raise ValidationError({"department": ["Department is required."]})

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise ValidationError({"department": ["Invalid department ID."]})
    else:
        department = actor.department

    # --------------------------------------------------
    # 3️⃣ Resolve Allowed Roles (once)
    # --------------------------------------------------
    allowed_roles = department.allowed_roles.all()

    # --------------------------------------------------
    # 4️⃣ Resolve Roles by UUID
    # --------------------------------------------------
    roles = Role.objects.filter(id__in=role_ids)

    found_role_ids = set(roles.values_list("id", flat=True))
    missing_roles = set(role_ids) - found_role_ids

    
    if missing_roles:
        raise ValidationError({"roles": ["Some roles are invalid."]})

    # if not actor.is_superuser:
    #     allowed_role_ids = set(
    #         allowed_roles.values_list("id", flat=True)
    #     )
    #     invalid_roles = set(role_ids) - allowed_role_ids

    #     if invalid_roles:
    #         raise ValidationError(
    #             {"roles": ["Some roles are not allowed for this department."]}
    #         )

    allowed_role_ids = set(
    allowed_roles.values_list("id", flat=True)
    )

    invalid_roles = set(role_ids) - allowed_role_ids

    if invalid_roles:
        raise ValidationError(
            {"roles": ["Some roles are not allowed for this department."]}
        )

    # --------------------------------------------------
    # 5️⃣ Expand Role → Policies
    # --------------------------------------------------
    role_policy_ids = set(
        Policy.objects.filter(
            policy_roles__role__in=roles
        ).values_list("id", flat=True)
    )

    # --------------------------------------------------
    # 6️⃣ Resolve Direct Policies by UUID
    # --------------------------------------------------
    direct_policies = Policy.objects.filter(id__in=policy_ids)

    found_policy_ids = set(direct_policies.values_list("id", flat=True))
    missing_policies = set(policy_ids) - found_policy_ids

    if missing_policies:
        raise ValidationError({"policies": ["Some policies are invalid."]})

    direct_policy_ids = found_policy_ids

    # Department policy scope enforcement
    # if not actor.is_superuser:
    #     allowed_policy_ids = set(
    #         Policy.objects.filter(
    #             policy_roles__role__in=allowed_roles
    #         ).values_list("id", flat=True)
    #     )

    #     invalid_policies = direct_policy_ids - allowed_policy_ids

    #     if invalid_policies:
    #         raise ValidationError(
    #             {"policies": ["Some policies are not allowed for this department."]}
    #         )

    allowed_policy_ids = set(
    Policy.objects.filter(
        policy_roles__role__in=allowed_roles
    ).values_list("id", flat=True)
    )

    invalid_policies = direct_policy_ids - allowed_policy_ids

    if invalid_policies:
        raise ValidationError(
            {"policies": ["Some policies are not allowed for this department."]}
        )


    # --------------------------------------------------
    # 7️⃣ Merge Final Policies (Flattened Model)
    # --------------------------------------------------
    final_policy_ids = role_policy_ids | direct_policy_ids

    if not final_policy_ids:
        raise ValidationError(
            {"non_field_errors": ["User must have at least one policy."]}
        )

    final_policies = Policy.objects.filter(id__in=final_policy_ids)

    # --------------------------------------------------
    # 8️⃣ Create User
    # --------------------------------------------------
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        department=department,
        is_active=True,
    )

    # --------------------------------------------------
    # 9️⃣ Persist Flattened Policies
    # --------------------------------------------------
    UserPolicy.objects.bulk_create(
        [
            UserPolicy(user=user, policy=policy, assigned_by=actor)
            for policy in final_policies
        ]
    )

    # --------------------------------------------------
    # 🔟 Persist Roles (Reporting Only)
    # --------------------------------------------------
    if roles:
        UserRole.objects.bulk_create(
            [
                UserRole(user=user, role=role, assigned_by=actor)
                for role in roles
            ]
        )

    return user




# 🔥 What This Version Fixes

# ✔ Superuser full bypass
# ✔ Admin department restriction
# ✔ Scope enforcement for roles
# ✔ Scope enforcement for policies
# ✔ Flattened policy storage
# ✔ Role storage for reporting
# ✔ Reduced redundant queries
# ✔ Atomic transaction
# ✔ Bulk insert for performance
# ✔ Explicit missing role/policy detection






# from django.db import transaction
# from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError

# from apps.department.models import Department
# from apps.access.models import Policy,UserPolicy
# from apps.access.services.role_services.role_validation import validate_role_assignment
# from apps.access.services.role_services.role_assignment import assign_roles_to_user

# User = get_user_model()

# @transaction.atomic
# def create_user(
#     *,
#     actor,
#     username: str,
#     password: str,
#     department_code: str,
#     role_codes: list[str] | None = None,
#     policy_codes: list[str] | None = None,
#     email: str | None = None,
# ):
#     role_codes = role_codes or []
#     policy_codes = policy_codes or []

#     if not role_codes and not policy_codes:
#         raise ValidationError(
#             {"non_field_errors": ["At least one role or policy is required."]}
#         )

#     if User.objects.filter(username=username).exists():
#         raise ValidationError({"username": ["Username already exists."]})

#     # 1️⃣ Resolve department
#     try:
#         department = Department.objects.get(code=department_code)
#     except Department.DoesNotExist:
#         raise ValidationError({"department": ["Invalid department."]})

#     # 2️⃣ Validate roles allowed by department
#     allowed_role_codes = set(
#         department.allowed_roles.values_list("code", flat=True)
#     )

#     invalid_roles = set(role_codes) - allowed_role_codes

#     if invalid_roles:
#         raise ValidationError(
#             {
#                 "roles": [
#                     f"Role(s) {sorted(invalid_roles)} "
#                     f"are not allowed for department '{department.code}'."
#                 ]
#             }
#         )

#     # 3️⃣ Expand role → policies
#     role_policy_codes = set(
#         Policy.objects
#         .filter(policy_roles__role__code__in=role_codes)
#         .values_list("code", flat=True)
#     )

#     # 4️⃣ Validate direct policies
#     direct_policy_codes = set()

#     if policy_codes:
#         existing_policies = set(
#             Policy.objects
#             .filter(code__in=policy_codes)
#             .values_list("code", flat=True)
#         )

#         missing = set(policy_codes) - existing_policies
#         if missing:
#             raise ValidationError(
#                 {"policies": [f"Invalid policies: {sorted(missing)}."]}
#             )

#         allowed_policies = set(
#             Policy.objects
#             .filter(policy_roles__role__in=department.allowed_roles.all())
#             .values_list("code", flat=True)
#         )

#         invalid_policies = set(policy_codes) - allowed_policies

#         if invalid_policies:
#             raise ValidationError(
#                 {
#                     "policies": [
#                         f"Policy(s) {sorted(invalid_policies)} "
#                         f"are not allowed for department '{department.code}'."
#                     ]
#                 }
#             )

#         direct_policy_codes = existing_policies

#     # 5️⃣ Merge final policy set
#     final_policy_codes = role_policy_codes | direct_policy_codes

#     if not final_policy_codes:
#         raise ValidationError(
#             {"non_field_errors": ["User must have at least one policy."]}
#         )

#     # 6️⃣ Create user
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email or "",
#         department=department,
#         is_active=True,
#     )

#     # 7️⃣ Persist policies
#     policies = Policy.objects.filter(code__in=final_policy_codes)

#     UserPolicy.objects.bulk_create(
#         [
#             UserPolicy(user=user, policy=policy)
#             for policy in policies
#         ]
#     )

#     return user

