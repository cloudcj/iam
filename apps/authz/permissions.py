# identity/permissions/has_permission.py

from django.conf import settings


from rest_framework.permissions import BasePermission

# class HasPermission(BasePermission):
#     """
#     Checks required_permission against JWT claims.
#     Used for IAM admin authorization.
#     """

#     def has_permission(self, request, view):
#         required_permission = getattr(view, "required_permission", None)

#         if not required_permission:
#             return True

#         claims = request.auth
#         if not isinstance(claims, dict):
#             return False

#         permissions = claims.get("permissions", [])
#         return required_permission in permissions



class HasPermission(BasePermission):
    def has_permission(self, request, view):
        # print("AUTH:", request.auth)
        # print("REQUIRED:", getattr(view, "required_permission", None))

        if not request.auth:
            return False

        perms = request.auth.get("permissions", [])
        print("TOKEN PERMS:", perms)

        return view.required_permission in perms






# import logging
# from rest_framework.permissions import BasePermission

# logger = logging.getLogger(__name__)

# class HasPermission(BasePermission):
#     def has_permission(self, request, view):
#         required = getattr(view, "required_permission", None)

#         # No permission required
#         if not required:
#             return True

#         token = request.auth  # validated JWT (dict-like)

#         sub = token.get("sub")
#         jti = token.get("jti")

#         permissions = token.get("permissions", [])

#         allowed = required in permissions

#         # 🔐 Safe audit log
#         logger.info(
#             "AUTHZ sub=%s jti=%s required=%s allowed=%s",
#             sub,
#             jti,
#             required,
#             allowed,
#         )

#         return allowed
