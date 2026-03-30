# # from django.db.models import Q
# # from django.core.exceptions import PermissionDenied

# # from apps.identity.models import User
# # from apps.common.helpers.authz.role_helpers import is_super_admin, is_iam_admin


# # def list_users(
# #     *,
# #     actor,
# #     department_code: str | None = None,
# #     role_code: str | None = None,
# #     is_active: bool | None = None,
# #     search: str | None = None,
# # ):
# #     """
# #     IAM-safe user listing.
# #     """

# #     qs = User.objects.all()

# #     # 🔐 VISIBILITY SCOPE (hard limit)
# #     if is_super_admin(actor):
# #         pass  # full access

# #     elif is_iam_admin(actor):
# #         dept = actor.user_department.first()
# #         if not dept:
# #             return User.objects.none()

# #         qs = qs.filter(
# #             user_department__department=dept.department
# #         )

# #         # Optional: prevent IAM admin from listing self
# #         qs = qs.exclude(id=actor.id)

# #     else:
# #         raise PermissionDenied("Not allowed to list users")

# #     # 🔎 FILTERS (scope reducers only)
# #     if is_active is not None:
# #         qs = qs.filter(is_active=is_active)

# #     if department_code:
# #         qs = qs.filter(
# #             user_department__department__code=department_code
# #         )

# #     if role_code:
# #         qs = qs.filter(
# #             user_roles__role__code=role_code
# #         )

# #     if search:
# #         qs = qs.filter(
# #             Q(username__icontains=search) |
# #             Q(email__icontains=search)
# #         )

# #     return (
# #         qs
# #         .distinct()
# #         .order_by("username")
# #         .prefetch_related(
# #             "user_roles__role",
# #             "user_department__department",
# #         )
# #     )


# from django.db.models import Q
# from django.core.exceptions import PermissionDenied

# from apps.identity.models import User
# from seeders.constants import RoleCodes
# from apps.common.helpers.authz.role_helpers import is_super_admin, is_iam_admin
# from apps.common.constants import HIDDEN_FROM_IAM_ADMIN

# def list_users(
#     *,
#     actor,
#     department_code: str | None = None,
#     role_code: str | None = None,
#     is_active: bool | None = None,
#     search: str | None = None,
# ):
#     """
#     IAM-safe user listing with hierarchy visibility rules.
#     """

#     qs = User.objects.all()

#     # 🔐 VISIBILITY SCOPE (hard limit)
#     if is_super_admin(actor):
#         qs = qs.exclude(id=actor.id)

#     elif is_iam_admin(actor):
#         dept = actor.user_department.first()
#         if not dept:
#             return User.objects.none()

#         qs = qs.filter(
#             user_department__department=dept.department
#         )

#         # ❌ cannot see SUPER_ADMIN or co-IAM_ADMIN
#         qs = qs.exclude(
#             user_roles__role__code__in=HIDDEN_FROM_IAM_ADMIN
#         )

#         # ❌ cannot see self
#         qs = qs.exclude(id=actor.id)

#     else:
#         raise PermissionDenied("Not allowed to list users")

#     # 🔎 FILTERS (scope reducers only)
#     if is_active is not None:
#         qs = qs.filter(is_active=is_active)

#     if department_code:
#         qs = qs.filter(
#             user_department__department__code=department_code
#         )

#     if role_code:
#         qs = qs.filter(
#             user_roles__role__code=role_code
#         )

#     if search:
#         qs = qs.filter(
#             Q(username__icontains=search) |
#             Q(email__icontains=search)
#         )

#     return (
#         qs
#         .distinct()
#         .order_by("username")
#         .prefetch_related(
#             "user_roles__role",
#             "user_department__department",
#         )
#     )

from django.db.models import Q
from django.contrib.auth import get_user_model

from apps.common.constants import RoleCodes, HIDDEN_FROM_DEPARTMENT_ADMIN, HIDDEN_FROM_PLATFORM_ADMIN
from apps.common.helpers.authz.role_helpers import has_role

User = get_user_model()


def list_users(
    *,
    actor,
    search: str | None = None,
    is_active: bool | None = None,
    department_id: str | None = None,
    role_code: str | None = None,
):
    is_superuser = actor.is_superuser
    is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
    is_platform_viewer = has_role(actor, RoleCodes.PLATFORM_VIEWER)
    is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)
    is_dept_viewer = has_role(actor, RoleCodes.DEPT_VIEWER)

    # --------------------------------------------------
    # 🔐 VISIBILITY SCOPE — hard limit, cannot be
    #    overridden by filters
    # --------------------------------------------------
    if is_superuser:
        qs = User.objects.exclude(
            is_superuser=True  # excludes self + co-superusers
        ) 

    elif is_platform_admin or is_platform_viewer:
        # All users across all departments
        # but cannot see other platform-level users
        qs = User.objects.exclude(
            user_roles__role__code__in=HIDDEN_FROM_PLATFORM_ADMIN
        )

    elif is_dept_admin or is_dept_viewer:
        # Own department only
        # Cannot see users with hidden roles (platform.admin, etc.)
        qs = (
            User.objects
            .filter(department=actor.department)
            .exclude(user_roles__role__code__in=HIDDEN_FROM_DEPARTMENT_ADMIN)
        )

    else:
        return User.objects.none()

    # Always exclude superusers from listing (only superuser sees superusers)
    if not is_superuser:
        qs = qs.exclude(is_superuser=True)

    # --------------------------------------------------
    # 🔎 FILTERS/SEARCH — scope reducers only
    # --------------------------------------------------
    if search:
        qs = qs.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) 
        )


    if is_active is not None:
        qs = qs.filter(is_active=is_active)

    if department_id:
        # Only superuser/platform can filter by department
        # dept admin is already scoped — ignore this filter
        if is_superuser or is_platform_admin or is_platform_viewer:
            qs = qs.filter(department__id=department_id)

    if role_code:
        qs = qs.filter(user_roles__role__code=role_code)

    return (
        qs
        .distinct()
        .order_by("username")
        .select_related("department")
        .prefetch_related(
            "user_roles__role",
            "user_roles__role__role_policies__policy",
        )
    )

