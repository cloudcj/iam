# # identity/views/delete_user_view.py

# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.exceptions import ValidationError

# from apps.identity.models import User
# from apps.authz.permissions import HasPermission
# from seeder.constants import IAMPermissions
# from ...services.user.delete import soft_delete_user


# class DeleteUserView(APIView):
#     permission_classes = [HasPermission]
#     required_permission = IAMPermissions.USER_UPDATE

#     def delete(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)

#         # IAM safety rule: no self-delete
#         if request.user.id == user.id:
#             return Response(
#                 {"detail": "You cannot delete your own account"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         try:
#             soft_delete_user(user=user)
#         except ValidationError as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.identity.models import User
from apps.identity.services.user.delete import soft_delete_user
from apps.authz.permissions import HasPermission
from seeder.constants import IAMPermissions


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_DELETE

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        soft_delete_user(
            actor=request.user,
            target=user,
        )

        return Response(
            {"status": "user deactivated"},
            status=status.HTTP_204_NO_CONTENT,
        )
