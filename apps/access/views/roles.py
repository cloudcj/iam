# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from apps.access.models.role import Role

# class ListRolesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         roles = Role.objects.prefetch_related(
#             'role_policies__policy__policy_permissions__permission'
#         ).all().order_by('code')
#         data = []
#         for r in roles:
#             policies = [
#                 {
#                     "id": str(rp.policy.id),
#                     "code": rp.policy.code,
#                     "name": rp.policy.name,
#                     "system": rp.policy.system,
#                     "resource": rp.policy.resource,
#                     "description": rp.policy.description,
#                     "permission_codes": [
#                         pp.permission.code
#                         for pp in rp.policy.policy_permissions.all()
#                     ],
#                 }
#                 for rp in r.role_policies.all()
#             ]
#             systems = list(dict.fromkeys(p["system"] for p in policies))
#             data.append({
#                 "id": str(r.id),
#                 "code": r.code,
#                 "name": r.name,
#                 "system": systems[0] if systems else r.code.split(".")[0],
#                 "policies": policies,
#             })
#         return Response(data)

# from rest_framework.views import APIView
# ... (keep all existing commented code)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.access.models.role import Role
from apps.department.models import Department
from apps.common.helpers.authz.role_helpers import has_role
from apps.common.constants import RoleCodes

MANAGEMENT_SYSTEMS = {"platform", "department"}
META_SYSTEMS = {"iam"}


class ListRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Role.objects.prefetch_related(
            'role_policies__policy__policy_permissions__permission'
        ).all().order_by('code')

        system = request.query_params.get("system")
        if system:
            queryset = queryset.filter(system=system)

        data = []
        for r in queryset:
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


class RoleFormOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        department_id = request.query_params.get("department")

        is_superuser = user.is_superuser
        is_platform_admin = not is_superuser and has_role(user, RoleCodes.PLATFORM_ADMIN)
        is_dept_admin = not is_superuser and not is_platform_admin

        # Determine if selected department is GLOBAL
        is_global = False
        if department_id:
            try:
                dept = Department.objects.get(id=department_id)
                is_global = dept.code == "GLOBAL"
            except Department.DoesNotExist:
                pass

        all_roles = Role.objects.prefetch_related(
            "role_policies__policy__policy_permissions__permission"
        ).order_by("name")

        # Management roles — filtered by who the requesting user is
        # and whether the selected department is GLOBAL
        mgmt_prefixes = []
        if is_superuser:
            mgmt_prefixes = ["platform."] if is_global else ["platform.", "department."]
        elif is_platform_admin:
            mgmt_prefixes = [] if is_global else ["department."]
        # dept admin gets no management roles

        def policy_data(rp):
            return {
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

        management_roles = []
        system_role_map: dict = {}

        for r in all_roles:
            system = r.code.split(".")[0]
            policies = [policy_data(rp) for rp in r.role_policies.all()]
            if system in MANAGEMENT_SYSTEMS:
                if any(r.code.startswith(p) for p in mgmt_prefixes):
                    grants = list(dict.fromkeys(
                        rp.policy.system
                        for rp in r.role_policies.all()
                        if rp.policy.system not in META_SYSTEMS
                    ))
                    management_roles.append({
                        "id": str(r.id),
                        "code": r.code,
                        "name": r.name,
                        "grants_systems": grants,
                        "policies": policies,
                    })
            else:
                if system not in system_role_map:
                    system_role_map[system] = []
                system_role_map[system].append({
                    "id": str(r.id),
                    "code": r.code,
                    "name": r.name,
                    "policies": policies,
                })

        return Response({
            "management_roles": management_roles,
            "system_roles": system_role_map,
        })
