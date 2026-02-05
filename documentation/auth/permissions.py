#from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

# class GaiaPermission(BasePermission):
#     """
#     Checks required_permission against JWT claims.
#     """

#     def has_permission(self, request, view):
#         required = getattr(view, "required_permission", None)

#         # No permission required → allow
#         if not required:
#             return True

#         # Authentication should already have run
#         claims = request.auth or {}
#         perms = claims.get("permissions", [])

#         return required in perms

from rest_framework.permissions import BasePermission


class GaiaPermission(BasePermission):
    """
    Checks required_permission against JWT access token claims.
    """

    def has_permission(self, request, view):
        required = getattr(view, "required_permission", None)

        # No permission required → allow
        if not required:
            return True

        # Authentication must already have run
        claims = request.auth
        if not claims:
            return False

        permissions = claims.get("permissions", [])

        return required in permissions
