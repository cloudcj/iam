from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.department.models import Department


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
