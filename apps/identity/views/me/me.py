from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authz.services.authorization_service import AuthorizationService


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token = request.auth

        if user.is_superuser:
            # Superuser — is_superuser flag handles all frontend checks
            # No need to load or return permissions
            permission_codes = set()
        else:
            # Regular user — read permissions from JWT (no DB hit)
            permission_codes = set(token.get("permissions", []))

        systems = sorted({code.split(".")[0] for code in permission_codes})

        return Response({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "department": {
                "code": user.department.code,
                "name": user.department.name,
            },
            "systems": systems,
            "permissions": sorted(permission_codes),
        })

























# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from apps.authz.services.authorization_service import AuthorizationService


# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         token = request.auth

#         # ✅ Read permissions from JWT (no DB hit)
#         if user.is_superuser:
#             # Superuser — load from DB since JWT carries empty permissions[]
#             permission_codes = AuthorizationService.get_user_permission_codes(user)
#         else:
#             permission_codes = set(token.get("permissions", []))

#         # Derive systems from permission codes
#         systems = sorted({code.split(".")[0] for code in permission_codes})

#         return Response({
#             "id": str(user.id),
#             "username": user.username,
#             "email": user.email,
#             "is_superuser": user.is_superuser,
#             "department": {
#                 "code": user.department.code,
#                 "name": user.department.name,
#             },
#             "systems": systems,
#             "permissions": sorted(permission_codes),
#         })

#################################################################

# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from apps.authz.services.authorization_service import AuthorizationService


# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         token = request.auth

#         # ✅ Read permissions from JWT (no DB hit)
#         if user.is_superuser:
#             # Superuser — load from DB since JWT carries empty permissions[]
#             permission_codes = AuthorizationService.get_user_permission_codes(user)
#         else:
#             permission_codes = set(token.get("permissions", []))

#         # ✅ Group permissions for frontend nav
#         grouped = AuthorizationService.group_permissions_by_system(permission_codes)

#         return Response({
#             "id": str(user.id),
#             "username": user.username,
#             "email": user.email,
#             "is_superuser": user.is_superuser,
#             "department": {
#                 "code": user.department.code,
#                 "name": user.department.name,
#             },
#             "systems": sorted(grouped.keys()),
#             "permissions": grouped,
#         })

####################################################################

# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from apps.authz.services.authorization_service import AuthorizationService
# from registry.systems import PERMISSION_REGISTRY


# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         token = request.auth

#         # ✅ Read permissions from JWT (no DB hit)
#         if user.is_superuser:
#             # Superuser — load from DB since JWT carries empty permissions[]
#             permission_codes = AuthorizationService.get_user_permission_codes(user)
#         else:
#             permission_codes = set(token.get("permissions", []))

#         # ✅ Group permissions for frontend nav
#         grouped = AuthorizationService.group_permissions_by_system(permission_codes)

#         # ✅ Systems with proper labels from registry
#         systems = [
#             {
#                 "code": code,
#                 "name": PERMISSION_REGISTRY[code].label if code in PERMISSION_REGISTRY else code.capitalize(),
#             }
#             for code in sorted(grouped.keys())
#         ]

#         return Response({
#             "id": str(user.id),
#             "username": user.username,
#             "email": user.email,
#             "is_superuser": user.is_superuser,
#             "department": {
#                 "code": user.department.code,
#                 "name": user.department.name,
#             },
#             "systems": systems,
#             "permissions": grouped,
#         })
