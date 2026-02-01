from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from apps.authz.permissions import HasPermission
from apps.identity.services.user import create_user

from seeder.constants import IAMPermissions

from apps.identity.serializers.user import UserCreateSerializer


class CreateUserView(APIView):
    permission_classes = [HasPermission]
    required_permission = IAMPermissions.USER_CREATE

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            user = create_user(
                username=data["username"],
                password=data["password"],
                email=data.get("email"),
                department_code=data["department"],
                role_codes=data["roles"],
            )
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"status":"User created successfully"},
            status=status.HTTP_201_CREATED,
        )
