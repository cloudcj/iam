# #from rest_framework.permissions import BasePermission
# from rest_framework.permissions import BasePermission
# from django.core.exceptions import PermissionDenied


# class HasPermission(BasePermission):
#     """
#     Checks required_permission against JWT access token claims.
#     """

#     def has_permission(self, request, view):
#         # 🔐 Must be authenticated first
#         if not request.user or not request.user.is_authenticated:
#             return False

#         # 🔑 Superuser / system override (recommended)
#         if getattr(request.user, "is_superuser", False):
#             return True

#         required = getattr(view, "required_permission", None)

#         # No permission required → allow
#         if not required:
#             return True

#         token = request.auth
#         if not token:
#             return False

#         # SimpleJWT tokens are dict-like, but be defensive
#         try:
#             permissions = token.get("permissions", [])
#         except AttributeError:
#             permissions = token.payload.get("permissions", [])

#         return required in permissions

from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    Checks required_permission against JWT access token claims.
    """

    def has_permission(self, request, view):
        # 🔐 Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        required = getattr(view, "required_permission", None)

        # No permission required → allow
        if not required:
            return True

        claims = request.auth or {}
        permissions = claims.get("permissions", [])

        return required in permissions

