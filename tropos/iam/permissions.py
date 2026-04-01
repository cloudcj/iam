from rest_framework.permissions import BasePermission


# class HasPermission(BasePermission):
#     """
#     Checks request.auth (validated JWT) for a required permission code.

#     Usage on any view:
#         required_permission = "inventory.device.read"
#     """

#     def has_permission(self, request, view):
#         if not request.user or not request.user.is_authenticated:
#             return False

#         required = getattr(view, "required_permission", None)
#         if not required:
#             return True  # No restriction declared — allow

#         token = request.auth
#         if not token:
#             return False

#         # Superuser bypass (is_superuser embedded in JWT sub lookup — check claim)
#         if getattr(request.user, "is_superuser", False):
#             return True

#         permissions = token.get("permissions", [])
#         return required in permissions

class HasPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        required = getattr(view, "required_permission", None)
        if not required:
            return True

        token = request.auth
        if not token:
            return False

        # Superuser bypass via JWT claim
        if token.get("is_superuser", False):
            return True

        permissions = token.get("permissions", [])
        return required in permissions
