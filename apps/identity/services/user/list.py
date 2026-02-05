# from django.db.models import Q
# from django.core.exceptions import PermissionDenied

# from apps.identity.models import User
# from apps.common.helpers.authz.role_helpers import is_super_admin, is_iam_admin


# def list_users(
#     *,
#     actor,
#     department_code: str | None = None,
#     role_code: str | None = None,
#     is_active: bool | None = None,
#     search: str | None = None,
# ):
#     """
#     IAM-safe user listing.
#     """

#     qs = User.objects.all()

#     # 🔐 VISIBILITY SCOPE (hard limit)
#     if is_super_admin(actor):
#         pass  # full access

#     elif is_iam_admin(actor):
#         dept = actor.user_department.first()
#         if not dept:
#             return User.objects.none()

#         qs = qs.filter(
#             user_department__department=dept.department
#         )

#         # Optional: prevent IAM admin from listing self
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
from django.core.exceptions import PermissionDenied

from apps.identity.models import User
from seeder.constants import RoleCodes
from apps.common.helpers.authz.role_helpers import is_super_admin, is_iam_admin
from apps.common.constants import HIDDEN_FROM_IAM_ADMIN

def list_users(
    *,
    actor,
    department_code: str | None = None,
    role_code: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
):
    """
    IAM-safe user listing with hierarchy visibility rules.
    """

    qs = User.objects.all()

    # 🔐 VISIBILITY SCOPE (hard limit)
    if is_super_admin(actor):
        qs = qs.exclude(id=actor.id)

    elif is_iam_admin(actor):
        dept = actor.user_department.first()
        if not dept:
            return User.objects.none()

        qs = qs.filter(
            user_department__department=dept.department
        )

        # ❌ cannot see SUPER_ADMIN or co-IAM_ADMIN
        qs = qs.exclude(
            user_roles__role__code__in=HIDDEN_FROM_IAM_ADMIN
        )

        # ❌ cannot see self
        qs = qs.exclude(id=actor.id)

    else:
        raise PermissionDenied("Not allowed to list users")

    # 🔎 FILTERS (scope reducers only)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)

    if department_code:
        qs = qs.filter(
            user_department__department__code=department_code
        )

    if role_code:
        qs = qs.filter(
            user_roles__role__code=role_code
        )

    if search:
        qs = qs.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    return (
        qs
        .distinct()
        .order_by("username")
        .prefetch_related(
            "user_roles__role",
            "user_department__department",
        )
    )
