from apps.identity.models import User
from django.db.models import Q


def list_users(
    *,
    department_code: str | None = None,
    role_code: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
):
    """
    List users with optional filters.

    Filters:
    - department_code: filter by department code
    - role_code: filter by role code
    - is_active: filter active / inactive users
    - search: partial match on username or email
    """

    qs = User.objects.all()

    if is_active is not None:
        qs = qs.filter(is_active=is_active)

    if department_code:
        qs = qs.filter(
            userdepartment__department__code=department_code
        )

    if role_code:
        qs = qs.filter(
            userrole__role__code=role_code
        )

    if search:
        qs = qs.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    return qs.distinct().order_by("username")

