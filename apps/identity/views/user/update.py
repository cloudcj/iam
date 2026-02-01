from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import User
from apps.authz.permissions import HasPermission
from seeder.constants import IAMPermissions

from ...serializers.user import UpdateUserInfoSerializer,UpdateUserDepartmentSerializer
from ...services.user import update_user_basic,update_user_department

class UpdateUserInfoView(APIView):
    permission_classes = [HasPermission]
    required_permission = IAMPermissions.USER_UPDATE

    def patch(self, request, user_id):
        serializer = UpdateUserInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = update_user_basic(
                user_id=user_id,
                **serializer.validated_data,
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
            }
        )


class UpdateUserDepartmentView(APIView):
    permission_classes = [HasPermission]
    required_permission = IAMPermissions.USER_UPDATE            #IAMPermissions.USER_CHANGE_DEPARTMENT

    def patch(self, request, user_id):
        serializer = UpdateUserDepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(id=user_id)
            update_user_department(
                user=user,
                department_code=serializer.validated_data["department"],
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

        return Response(status=204)
    
from ...serializers.user import UpdateUserRoleSerializer
from ...services.user import update_user_role
from django.shortcuts import get_object_or_404
from rest_framework import status

class UpdateUserRolesView(APIView):
    permission_classes = [HasPermission]
    required_permission = IAMPermissions.USER_ASSIGN_ROLE

    def patch(self, request, user_id):
        serializer = UpdateUserRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, id=user_id)

        try:
            update_user_role(
                user=user,
                role_codes=serializer.validated_data["roles"],
            )
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "User role updated successfully" },status=status.HTTP_204_NO_CONTENT)