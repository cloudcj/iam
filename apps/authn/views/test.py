# accounts/views/test.py
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.authz.permissions import HasPermission
from seeder.constants import InventoryPermissions
from apps.authn.authentication import IAMAuthentication

class ProtectedTestView(APIView):
    authentication_classes = [IAMAuthentication]
    permission_classes = [HasPermission]
    required_permission = InventoryPermissions.READ

    def get(self, request):
        perms = request.auth.get("permissions", []) if request.auth else []

        return Response({
            "user": str(request.user),
            "is_authenticated": request.user.is_authenticated,
            "auth": request.auth.payload if request.auth else None,  # ✅ CORRECT
            "required": self.required_permission,
            "allowed": self.required_permission in perms,
        })



# class ProtectedTestView(APIView):

#     permission_classes = [HasPermission]
#     required_permission = InventoryPermissions.READ

#     def get(self, request):
#         return Response({
#             "user": request.user.username,
#             "permissions": request.auth.get("permissions", []),
#         })

# from iam.services.users import create_user, assign_department
# from iam.services.assignments import assign_role_to_user

# # 1. Create user
# user = create_user(
#     username="monitor",
#     email="monitore@gaia.io",
#     password="TempPass123",
# )

# # 2. Assign department
# assign_department(
#     user=user,
#     department_code="PLATFORM",
# )

# # 3. Assign role (validated)
# assign_role_to_user(
#     user=user,
#     role_name="InventoryViewer",
# )