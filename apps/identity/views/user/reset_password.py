from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.authn.authentication import IAMAuthentication
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions
from apps.common.constants import RoleCodes
from apps.common.helpers.authz.role_helpers import has_role

from apps.audit.mixins import AuditMixin
from apps.audit.models import AuditLog

from ...serializers.user.reset_password import ResetPasswordSerializer

User = get_user_model()


class ResetUserPasswordView(AuditMixin, APIView):

    audit_action = AuditLog.Action.USER_RESET_PASSWORD
    audit_target_type = "user"

    def get_audit_target_id(self, request, response):
        return self.kwargs.get("user_id")

    def get_audit_detail(self, request, response):
        return {"reset_by": request.user.username}

    authentication_classes = [IAMAuthentication]
    permission_classes = [HasPermission]
    required_permission = IAMPermissions.USER_RESET_PASSWORD

    def post(self, request, user_id):
        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        actor = request.user

        # Only superuser can reset another superuser's password
        if target.is_superuser and not actor.is_superuser:
            return Response(
                {"detail": "You do not have permission to reset a superuser's password."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Platform admin cannot reset another platform admin's password
        if not actor.is_superuser and has_role(actor, RoleCodes.PLATFORM_ADMIN) and has_role(target, RoleCodes.PLATFORM_ADMIN):
            return Response(
                {"detail": "You do not have permission to reset another platform admin's password."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Department admins can only reset passwords for users in their own department
        if not actor.is_superuser and not has_role(actor, RoleCodes.PLATFORM_ADMIN):
            if target.department_id != actor.department_id:
                return Response(
                    {"detail": "You can only reset passwords for users in your department."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target.set_password(serializer.validated_data["new_password"])
        target.must_change_password = True
        target.save(update_fields=["password", "must_change_password"])

        return Response({"detail": "Password reset successfully."})
