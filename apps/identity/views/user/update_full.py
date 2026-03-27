# from django.core.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from ...models import User
# from apps.authz.permissions import HasPermission
# from seeder.constants import IAMPermissions

# from ...serializers.user import UpdateUserInfoSerializer,UpdateUserDepartmentSerializer
# from ...services.user import update_user_basic,update_user_department

# class UpdateUserInfoView(APIView):
#     permission_classes = [HasPermission]
#     required_permission = IAMPermissions.USER_UPDATE

#     def patch(self, request, user_id):
#         serializer = UpdateUserInfoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             user = update_user_basic(
#                 user_id=user_id,
#                 **serializer.validated_data,
#             )
#         except ValidationError as e:
#             return Response({"detail": str(e)}, status=400)

#         return Response(
#             {
#                 "id": str(user.id),
#                 "username": user.username,
#                 "email": user.email,
#                 "is_active": user.is_active,
#             }
#         )


# class UpdateUserDepartmentView(APIView):
#     permission_classes = [HasPermission]
#     required_permission = IAMPermissions.USER_UPDATE            #IAMPermissions.USER_CHANGE_DEPARTMENT

#     def patch(self, request, user_id):
#         serializer = UpdateUserDepartmentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             user = User.objects.get(id=user_id)
#             update_user_department(
#                 user=user,
#                 department_code=serializer.validated_data["department"],
#             )
#         except ValidationError as e:
#             return Response({"detail": str(e)}, status=400)

#         return Response(status=204)
    
# from ...serializers.user import UpdateUserRoleSerializer
# from ...services.user import update_user_role
# from django.shortcuts import get_object_or_404
# from rest_framework import status

# class UpdateUserRolesView(APIView):
#     permission_classes = [HasPermission]
#     required_permission = IAMPermissions.USER_ASSIGN_ROLE

#     def patch(self, request, user_id):
#         serializer = UpdateUserRoleSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = get_object_or_404(User, id=user_id)

#         try:
#             update_user_role(
#                 user=user,
#                 role_codes=serializer.validated_data["roles"],
#             )
#         except ValidationError as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response({"message": "User role updated successfully" },status=status.HTTP_204_NO_CONTENT)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from apps.identity.models import User
from apps.identity.serializers.user.update import UpdateUserSerializer
from apps.identity.services.user.update.full import update_user
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions


class UpdateUserFullView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_UPDATE

    def patch(self, request, user_id):
        target = get_object_or_404(User, id=user_id)

        serializer = UpdateUserSerializer(
            data=request.data,
            context={"user_id": user_id}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = update_user(
                actor=request.user,
                target=target,
                username=data.get("username") if request.user.is_superuser else None,
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                is_active=data.get("is_active", True),
                department_id=data["department"],
                role_ids=data["roles"],
                permission_ids=data.get("permission_ids", []),
            )
        except IntegrityError as e:
            if "email" in str(e):
                return Response({"email": ["A user with that email already exists."]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "A database conflict occurred."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "id": str(user.id),
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
        }, status=status.HTTP_200_OK)
