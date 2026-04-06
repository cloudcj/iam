from rest_framework.permissions import BasePermission


class BlockIfMustChangePassword(BasePermission):
    """
    Blocks access unless the user has changed their password.
    Reads must_change_password from JWT token.
    Allows bypass via view attribute bypass_must_change_password=True.
    """

    message = {
        "detail": "You must change your password before accessing this resource.",
        "code": "must_change_password",
    }

    def has_permission(self, request, view):
        # Allow the view to bypass this check (e.g., ChangePasswordView)
        if getattr(view, "bypass_must_change_password", False):
            return True

        # 🔐 Check JWT token for must_change_password flag
        token = request.auth
        if token and token.get("must_change_password"):
            return False

        return True


class HasPermission(BasePermission):
    """
    Checks required_permission against JWT permissions[] claim.
    No DB hit — reads directly from token.
    """

    def has_permission(self, request, view):
        # 🔐 Must be authenticated
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        # No permission required → allow
        required = getattr(view, "required_permission", None)
        if not required:
            return True

        # 🔐 Superuser bypasses all checks
        if getattr(user, "is_superuser", False):
            return True

        # 🔐 Read permissions from JWT token (no DB hit)
        token = request.auth
        if not token:
            return False

        permissions = token.get("permissions", [])
        return required in permissions


# class HasPermission(BasePermission):
#     """
#     Checks required_permission against IAM authorization logic.
#     """

#     def has_permission(self, request, view):
#         # 🔐 Must be authenticated
#         user = getattr(request, "user", None)
#         if not user or not user.is_authenticated:
#             return False

#         # View declares required permission
#         required = getattr(view, "required_permission", None)

#         # No permission required → allow
#         if not required:
#             return True

#         # 🔐 Superadmin shortcut (optional but recommended)
#         if getattr(user, "is_superuser", False):
#             return True

#         # 🔐 Delegate to IAM logic
#         return user.has_permission(required)

