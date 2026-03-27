from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.access.models.role import Role
from apps.access.models.role_policy import RolePolicy


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
            data.append({
                "id": str(r.id),
                "code": r.code,
                "name": r.name,
                "system": r.code.split(".")[0],
                "policies": policies,
            })
        return Response(data)


##################

from apps.access.models.policy import Policy
from apps.access.models.permission import Permission


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
