from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from apps.department.models import Department
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions

from apps.audit.mixins import AuditMixin
from apps.audit.models import AuditLog

from ._helpers import dept_data, set_allowed_systems


class UpdateDepartmentView(AuditMixin, APIView):

    audit_action = AuditLog.Action.DEPT_UPDATE
    audit_target_type = "department"

    def get_audit_target_id(self, request, response):
        return self.kwargs.get("department_id")

    def get_audit_detail(self, request, response):
        return {"name": request.data.get("name")}

    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.DEPARTMENT_UPDATE

    @transaction.atomic
    def patch(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)

        if department.code == "GLOBAL" and not request.user.is_superuser:
            return Response({"detail": "Only superusers can edit the GLOBAL department."}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get("name", department.name).strip().title()
        allowed_systems = request.data.get("allowed_systems", None)

        if not name:
            return Response({"name": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if allowed_systems is not None and len(allowed_systems) == 0:
            return Response({"allowed_systems": ["At least one system is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if Department.objects.filter(name=name).exclude(id=department.id).exists():
            return Response({"name": ["A department with this name already exists."]}, status=status.HTTP_400_BAD_REQUEST)

        department.name = name
        department.save(update_fields=["name"])

        if allowed_systems is not None:
            set_allowed_systems(department, allowed_systems)

        return Response(dept_data(department))
