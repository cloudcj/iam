from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.department.models import Department
from ._helpers import dept_data


class ListDepartmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.prefetch_related("allowed_system_entries").all()
        return Response([dept_data(d) for d in departments])
