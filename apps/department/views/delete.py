from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.department.models import Department
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions

from apps.audit.mixins import AuditMixin
from apps.audit.models import AuditLog

class DeleteDepartmentView(AuditMixin, APIView):

    audit_action = AuditLog.Action.DEPT_DELETE
    audit_target_type = "department"

    def get_audit_detail(self, request, response):
        return {"name": getattr(self, "_dept_name", None)}

    def delete(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        self._dept_name = department.name   # capture before deletion

        if department.code == "GLOBAL":
            return Response({"detail": "The GLOBAL department cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        if department.users.exists():
            return Response({"detail": "Cannot delete a department that has users assigned to it."}, status=status.HTTP_400_BAD_REQUEST)

        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
