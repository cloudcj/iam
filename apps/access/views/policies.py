from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.access.models.policy import Policy


class ListPoliciesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        policies = Policy.objects.prefetch_related("policy_permissions__permission").all().order_by("system", "resource", "code")
        data = []
        for p in policies:
            data.append({
                "id": str(p.id),
                "code": p.code,
                "name": p.name,
                "system": p.system,
                "resource": p.resource,
                "description": p.description,
                "permission_codes": [
                    pp.permission.code
                    for pp in p.policy_permissions.all()
                ],
            })
        return Response(data)

