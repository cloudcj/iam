from django.db import transaction
from django.core.exceptions import ValidationError

from apps.identity.models import User
from apps.department.models import Department,UserDepartment
from apps.access.models import Role,UserRole,DepartmentAllowedRole

from django.db import transaction
from django.core.exceptions import ValidationError
from apps.identity.models import User

@transaction.atomic
def update_user_basic(*, user_id, email=None, is_active=None):
    try:
        user = User.objects.select_for_update().get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError("User not found")

    if email is not None:
        user.email = email

    if is_active is not None:
        user.is_active = is_active

    user.save()
    return user



@transaction.atomic
def update_user_department(*, user, department_code):
    try:
        department = Department.objects.get(code=department_code)
    except Department.DoesNotExist:
        raise ValidationError("Invalid department")

    UserDepartment.objects.update_or_create(
        user=user,
        defaults={"department": department},
    )



@transaction.atomic
def update_user_role(*, user: User, role_codes: list[str]):
    if not role_codes:
        raise ValidationError("User must have at least one role")

    # Ensure user has a department
    try:
        user_department = UserDepartment.objects.select_related("department").get(
            user=user
        )
    except UserDepartment.DoesNotExist:
        raise ValidationError("User has no department assigned")

    department = user_department.department

    # Fetch roles in one query
    roles = list(Role.objects.filter(code__in=role_codes))
    if len(roles) != len(set(role_codes)):
        raise ValidationError("One or more roles are invalid")

    # Allowed roles for department
    allowed_role_ids = set(
        DepartmentAllowedRole.objects.filter(
            department=department
        ).values_list("role_id", flat=True)
    )

    for role in roles:
        if role.id not in allowed_role_ids:
            raise ValidationError(
                f"Role '{role.code}' is not allowed in department '{department.code}'"
            )

    # Replace roles atomically
    UserRole.objects.filter(user=user).delete()
    UserRole.objects.bulk_create(
        [UserRole(user=user, role=role) for role in roles]
    )

    return True




# def list_users():
#     """
#     Return users with department and roles.
#     """

#     users = (
#         User.objects
#         .select_related()
#         .prefetch_related(
#             "user_department__department",
#             "user_roles__role",
#         )
#     )

#     results = []

#     for user in users:
#         # department = None
#         # if hasattr(user, "userdepartment"):
#         #     department = user.userdepartment.department.code
#         dept_link = user.user_department.first()
#         department = (
#             dept_link.department.name
#             if dept_link else None
#         )

#         roles = [
#             ur.role.code
#             for ur in user.user_roles.all()
#         ]

#         results.append({
#             "id": str(user.id),
#             "username": user.username,
#             "email": user.email,
#             "is_active": user.is_active,
#             "department": department,
#             "roles": roles,
#             "created_at": user.created_at,
#         })

#     return results




# @transaction.atomic
# def update_user_identity(
#     *,
#     user: User,
#     username: str | None = None,
#     email: str | None = None,
#     is_active: bool | None = None,
# ):
#     """
#     Update user identity fields safely.
#     """

#     if username:
#         # Prevent duplicate usernames
#         if User.objects.filter(username=username).exclude(id=user.id).exists():
#             raise ValidationError("Username already exists")
#         user.username = username

#     if email is not None:
#         user.email = email

#     if is_active is not None:
#         user.is_active = is_active

#     user.save(update_fields=["username", "email", "is_active"])

#     return user

# ##################################################################

# @transaction.atomic
# def update_user_roles(*, user: User, role_codes: list[str]):
#     """
#     Replace a user's roles with a new validated set.
#     """

#     if not role_codes:
#         raise ValidationError("User must have at least one role")

#     # 1️⃣ Ensure user has a department
#     try:
#         user_department = UserDepartment.objects.select_related("department").get(
#             user=user
#         )
#     except UserDepartment.DoesNotExist:
#         raise ValidationError("User has no department assigned")

#     department = user_department.department

#     # 2️⃣ Resolve roles + validate existence
#     roles = []
#     for role_code in role_codes:
#         try:
#             role = Role.objects.get(code=role_code)
#             roles.append(role)
#         except Role.DoesNotExist:
#             raise ValidationError(f"Invalid role: {role_code}")

#     # 3️⃣ Validate department → allowed roles
#     allowed_role_ids = set(
#         DepartmentAllowedRole.objects.filter(
#             department=department
#         ).values_list("role_id", flat=True)
#     )

#     for role in roles:
#         if role.id not in allowed_role_ids:
#             raise ValidationError(
#                 f"Role '{role.code}' is not allowed in department '{department.code}'"
#             )

#     # 4️⃣ Replace roles (atomic)
#     UserRole.objects.filter(user=user).delete()

#     UserRole.objects.bulk_create([
#         UserRole(user=user, role=role)
#         for role in roles
#     ])

#     return True


# #################################

# @transaction.atomic
# def update_user_department(*, user_id: str, department_code: str):
#     user = User.objects.get(id=user_id)
#     department = Department.objects.get(code=department_code)

#     # 1️⃣ update department
#     UserDepartment.objects.update_or_create(
#         user=user,
#         defaults={"department": department},
#     )

#     # 2️⃣ REMOVE ALL ROLES (NO VALIDATION)
#     UserRole.objects.filter(user=user).delete()

#     # 3️⃣ revoke refresh tokens
#     RefreshToken.objects.filter(
#         user=user,
#         is_revoked=False
#     ).update(is_revoked=True)

#     return user

# @transaction.atomic
# def update_user_department(*, user_id: str, department_code: str):
#     user = User.objects.get(id=user_id)
#     department = Department.objects.get(code=department_code)

#     # 1️⃣ get current roles
#     current_roles = (
#         UserRole.objects
#         .filter(user=user)
#         .select_related("role")
#     )

#     role_codes = {ur.role.code for ur in current_roles}

#     # 2️⃣ allowed roles for new department
#     allowed_roles = set(
#         DepartmentAllowedRole.objects
#         .filter(department=department)
#         .values_list("role__code", flat=True)
#     )

#     # 3️⃣ validate roles
#     invalid_roles = role_codes - allowed_roles
#     if invalid_roles:
#         raise ValidationError({
#             "roles": f"Roles not allowed in department {department.code}: {list(invalid_roles)}"
#         })

#     # 4️⃣ update department
#     UserDepartment.objects.update_or_create(
#         user=user,
#         defaults={"department": department},
#     )

#     # 5️⃣ revoke refresh tokens
#     RefreshToken.objects.filter(user=user, is_revoked=False)\
#         .update(is_revoked=True)

#     return user