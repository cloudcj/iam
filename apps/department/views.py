from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from apps.department.models import Department
from apps.access.models import DepartmentAllowedSystem
from apps.authz.permissions import HasPermission
from apps.common.constants.permission_codes import IAMPermissions


class ListDepartmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.prefetch_related('allowed_system_entries').all()
        data = [
            {
                "id": str(d.id),
                "code": d.code,
                "name": d.name,
                "allowed_systems": d.allowed_systems,
            }
            for d in departments
        ]
        return Response(data)


class CreateDepartmentView(APIView):
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

        code = name.strip().upper().replace(" ", "_")
        # ensure code uniqueness by appending a counter if needed
        base_code = code
        counter = 1
        while Department.objects.filter(code=code).exists():
            code = f"{base_code}_{counter}"
            counter += 1

        department = Department.objects.create(name=name, code=code)

        if allowed_systems:
            DepartmentAllowedSystem.objects.bulk_create([
                DepartmentAllowedSystem(department=department, system=s)
                for s in allowed_systems
            ], ignore_conflicts=True)

        return Response({
            "id": str(department.id),
            "code": department.code,
            "name": department.name,
            "allowed_systems": department.allowed_systems,
        }, status=status.HTTP_201_CREATED)


class UpdateDepartmentView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.DEPARTMENT_UPDATE

    @transaction.atomic
    def patch(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)

        if department.code == "GLOBAL":
            return Response({"detail": "The GLOBAL department cannot be edited."}, status=status.HTTP_400_BAD_REQUEST)

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
            DepartmentAllowedSystem.objects.filter(department=department).delete()
            if allowed_systems:
                DepartmentAllowedSystem.objects.bulk_create([
                    DepartmentAllowedSystem(department=department, system=s)
                    for s in allowed_systems
                ], ignore_conflicts=True)

        return Response({
            "id": str(department.id),
            "code": department.code,
            "name": department.name,
            "allowed_systems": department.allowed_systems,
        })


class DeleteDepartmentView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.DEPARTMENT_DELETE

    def delete(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)

        if department.code == "GLOBAL":
            return Response(
                {"detail": "The GLOBAL department cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if department.users.exists():
            return Response(
                {"detail": "Cannot delete a department that has users assigned to it."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
