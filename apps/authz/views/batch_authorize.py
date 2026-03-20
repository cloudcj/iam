

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# class BatchAuthorizeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         permissions = request.data.get("permissions", [])

#         if not isinstance(permissions, list):
#             return Response(
#                 {"detail": "permissions must be a list"},
#                 status=400,
#             )

#         user = request.user

#         allowed = [
#             perm for perm in permissions
#             if user.has_permission(perm)
#         ]

#         return Response({"allowed": allowed})
from apps.authz.services.authorization_service import AuthorizationService


class BatchAuthorizeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        permissions = request.data.get("permissions", [])

        if not isinstance(permissions, list):
            return Response(
                {"detail": "permissions must be a list"},
                status=400,
            )

        user = request.user

        # 🔥 OPTIMIZED: load all user permissions once
        user_permissions = AuthorizationService.get_user_permission_codes(user)

        allowed = [
            perm for perm in permissions
            if perm in user_permissions
        ]


        return Response({"allowed": allowed})




# class BatchAuthorizeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         permissions = request.data.get("permissions", [])

#         if not isinstance(permissions, list):
#             return Response(
#                 {"detail": "permissions must be a list"},
#                 status=400,
#             )

#         user = request.user

#         # # 🔎 DEBUG START
#         # print("---- BATCH AUTHORIZE DEBUG ----")
#         # print("User:", user.username)
#         # print("Permissions requested:", permissions)
#         # print(
#         #     "User policies:",
#         #     list(user.user_policies.values_list("policy__code", flat=True))
#         # )

#         # 🔥 OPTIMIZED: load all user permissions once
#         user_permissions = AuthorizationService.get_user_permission_codes(user)

#         allowed = [
#             perm for perm in permissions
#             if perm in user_permissions
#         ]

#         # print("Allowed result:", allowed)
#         # print("--------------------------------")

#         return Response({"allowed": allowed})
