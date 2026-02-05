from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.identity.models import User
from apps.identity.serializers.user import UpdateUserBasicSerializer
from apps.identity.services.user.update_basic import update_user_basic_info
from apps.authz.permissions import HasPermission
from seeder.constants import IAMPermissions


class UpdateUserBasicView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_UPDATE

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        serializer = UpdateUserBasicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_user_basic_info(
            actor=request.user,
            target=user,
            data=serializer.validated_data,
        )

        return Response(
            {"detail": "User updated successfully"},
            status=status.HTTP_200_OK,
        )
