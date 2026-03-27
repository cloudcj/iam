from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from apps.department.models import Department
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions

from apps.audit.mixins import AuditMixin
from apps.audit.models import AuditLog

from ._helpers import dept_data, set_allowed_systems


class CreateDepartmentView(AuditMixin, APIView):

    audit_action = AuditLog.Action.DEPT_CREATE
    audit_target_type = "department"

    def get_audit_target_id(self, request, response):
        return response.data.get("id") if response.status_code == 201 else None

    def get_audit_detail(self, request, response):
        return {"name": request.data.get("name")}

    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.DEPARTMENT_CREATE

    @transaction.atomic
    def post(self, request):
        name = request.data.get("name", "").strip().title()
        allowed_systems = request.data.get("allowed_systems", [])

        if not name:
            return Response({"name": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if not allowed_systems:
            return Response({"allowed_systems": ["At least one system is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if Department.objects.filter(name=name).exists():
            return Response({"name": ["A department with this name already exists."]}, status=status.HTTP_400_BAD_REQUEST)

        # ensure code uniqueness by appending a counter if needed
        base_code = name.upper().replace(" ", "_")
        code, counter = base_code, 1
        while Department.objects.filter(code=code).exists():
            code = f"{base_code}_{counter}"
            counter += 1

        department = Department.objects.create(name=name, code=code)
        set_allowed_systems(department, allowed_systems)

        return Response(dept_data(department), status=status.HTTP_201_CREATED)
