from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.access.models.role import Role
from apps.access.models.role_policy import RolePolicy


class ListRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.prefetch_related('role_policies__policy').all().order_by('code')
        data = []
        for r in roles:
            policies = [
                {
                    "id": str(rp.policy.id),
                    "code": rp.policy.code,
                    "name": rp.policy.name,
                    "system": rp.policy.system,
                    "resource": rp.policy.resource,
                    "description": rp.policy.description,
                }
                for rp in r.role_policies.all()
            ]
            data.append({
                "id": str(r.id),
                "code": r.code,
                "name": r.name,
                "system": r.code.split(".")[0],
                "policies": policies,
            })
        return Response(data)
