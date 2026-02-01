from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from apps.authz.permissions import HasPermission
from apps.identity.services.user import list_users

from seeder.constants import IAMPermissions


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...serializers.user import UserListSerializer
from ...services.user import list_users

class ListUsersView(APIView):
    permission_classes = [HasPermission]
    required_permission = IAMPermissions.USER_READ

    def get(self, request):
        users = list_users(
            department_code=request.query_params.get("department"),
            role_code=request.query_params.get("role"),
            is_active=request.query_params.get("is_active"),
            search=request.query_params.get("search"),
        )

        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
