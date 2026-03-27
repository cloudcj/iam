from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.access.models.role import Role

class ListRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.prefetch_related(
            'role_policies__policy__policy_permissions__permission'
        ).all().order_by('code')
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
                    "permission_codes": [
                        pp.permission.code
                        for pp in rp.policy.policy_permissions.all()
                    ],
                }
                for rp in r.role_policies.all()
            ]
            systems = list(dict.fromkeys(p["system"] for p in policies))
            data.append({
                "id": str(r.id),
                "code": r.code,
                "name": r.name,
                "system": systems[0] if systems else r.code.split(".")[0],
                "policies": policies,
            })
        return Response(data)