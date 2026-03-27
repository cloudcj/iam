from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.access.models.permission import Permission


class ListPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permissions = Permission.objects.all().order_by("system", "resource", "action")
        data = []
        for p in permissions:
            data.append({
                "id": str(p.id),
                "code": p.code,
                "system": p.system,
                "resource": p.resource,
                "action": p.action,
                "description": p.description,
            })
        return Response(data)