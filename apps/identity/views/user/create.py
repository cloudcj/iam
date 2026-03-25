# # apps/identity/views/user/create.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from apps.identity.serializers.user.create import UserCreateSerializer
# from apps.identity.services.user.create import create_user
# from apps.authz.permissions import HasPermission


# class CreateUserView(APIView):
#     permission_classes = [IsAuthenticated, HasPermission]
#     required_permission = "iam.user.create"

#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         data = serializer.validated_data

#         user = create_user(
#             actor=request.user,
#             username=data["username"],
#             password=data["password"],
#             email=data.get("email"),
#             department_id=data.get("department"),
#             role_ids=data.get("roles"),
#             policy_ids=data.get("policies"),
#         )

#         return Response(
#             {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "department": user.department.code,
#             },
#             status=status.HTTP_201_CREATED,
#         )

############################################################################
 
# apps/identity/views/user/create.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from apps.identity.serializers.user.create import UserCreateSerializer
# from apps.identity.services.user.create import create_user
# from apps.authz.permissions import HasPermission
# from apps.common.constants.permission_codes import IAMPermissions


# class CreateUserView(APIView):
#     permission_classes = [IsAuthenticated, HasPermission]
#     required_permission = IAMPermissions.USER_CREATE

#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         data = serializer.validated_data

#         user = create_user(
#             actor=request.user,
#             username=data["username"],
#             password=data["password"],
#             email=data.get("email"),
#             department_id=data.get("department"),
#             role_ids=data.get("roles", []),
#             extra_policy_ids=data.get("extra_policies", []),
#         )

#         return Response(
#             {
#                 "id": str(user.id),
#                 "username": user.username,
#                 "email": user.email,
#                 "department": {
#                     "id": str(user.department.id),
#                     "code": user.department.code,
#                     "name": user.department.name,
#                 },
#             },
#             status=status.HTTP_201_CREATED,
#         )

#################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.identity.serializers.user.create import UserCreateSerializer
from apps.identity.services.user.create import create_user
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions


class CreateUserView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_CREATE

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = create_user(
            actor=request.user,
            username=data["username"],
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            department_id=data.get("department"),
            role_ids=data.get("roles", []),
        )

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "department": {
                    "id": str(user.department.id),
                    "code": user.department.code,
                    "name": user.department.name,
                },
            },
            status=status.HTTP_201_CREATED,
        )