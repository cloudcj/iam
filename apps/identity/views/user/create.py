# apps/identity/views/user/create.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.identity.serializers.user.create import UserCreateSerializer
from apps.identity.services.user.create import create_user
from apps.authz.permissions import HasPermission


class CreateUserView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "iam.user.create"

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = create_user(
            actor=request.user,
            username=data["username"],
            password=data["password"],
            email=data.get("email"),
            department_id=data.get("department"),
            role_ids=data.get("roles"),
            policy_ids=data.get("policies"),
        )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "department": user.department.code,
            },
            status=status.HTTP_201_CREATED,
        )
