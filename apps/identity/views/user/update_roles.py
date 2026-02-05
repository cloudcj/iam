from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.identity.models import User
from apps.identity.serializers.user.update import UpdateUserRolesSerializer
from apps.identity.services.user.update_roles import update_user_roles
from apps.authz.permissions import HasPermission
from seeder.constants import IAMPermissions


class UpdateUserRolesView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_UPDATE

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        serializer = UpdateUserRolesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_user_roles(
            actor=request.user,
            target=user,
            role_codes=serializer.validated_data["roles"],
        )

        return Response(
            {"detail": "Roles updated successfully"},
            status=status.HTTP_200_OK,
        )
