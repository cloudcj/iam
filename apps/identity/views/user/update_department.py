from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.identity.models import User
from apps.identity.serializers.user import (
    UpdateUserDepartmentSerializer,
)
from apps.identity.services.user.update_department import update_user_department
from apps.authz.permissions import HasPermission
from seeder.constants import IAMPermissions


class UpdateUserDepartmentView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_UPDATE

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        serializer = UpdateUserDepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_user_department(
            actor=request.user,
            target=user,
            department_code=serializer.validated_data["department"],
        )

        return Response(
            {"detail": "Department updated successfully"},
            status=status.HTTP_200_OK,
        )
