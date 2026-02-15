# # accounts/views/test.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from apps.authz.permissions import HasPermission
# from seeder.constants import InventoryPermissions
# from apps.authn.authentication import IAMAuthentication

# class ProtectedTestView(APIView):
#     authentication_classes = [IAMAuthentication]
#     permission_classes = [HasPermission]
#     required_permission = InventoryPermissions.READ

#     def get(self, request):
#         perms = request.auth.get("permissions", []) if request.auth else []

#         return Response({
#             "user": str(request.user),
#             "is_authenticated": request.user.is_authenticated,
#             "auth": request.auth.payload if request.auth else None,  # ✅ CORRECT
#             "required": self.required_permission,
#             "allowed": self.required_permission in perms,
#         })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# class ProtectedTestView(APIView):
#     """
#     TEMPORARY TEST VIEW.
#     Used to manually test IAM authorization logic via Postman.
#     REMOVE after validation.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         permission = request.query_params.get("permission")

#         if not permission:
#             return Response(
#                 {"detail": "permission query param is required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         user = request.user

#         # Superadmin shortcut (current design)
#         if getattr(user, "is_superuser", False):
#             allowed = True
#         else:
#             allowed = user.has_permission(permission)

#         return Response(
#             {
#                 "user": user.username,
#                 "permission": permission,
#                 "allowed": allowed,
#             }
#         )



from apps.access.models import Permission

class ProtectedTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permission = request.query_params.get("permission")

        if not permission:
            return Response(
                {"detail": "permission query param is required"},
                status=400,
            )

        # ✅ validate permission exists
        if not Permission.objects.filter(code=permission).exists():
            return Response(
                {
                    "permission": permission,
                    "allowed": False,
                    "reason": "unknown permission",
                },
                status=200,
            )

        user = request.user

        if user.is_superuser:
            allowed = True
        else:
            allowed = user.has_permission(permission)

        return Response(
            {
                "user": user.username,
                "permission": permission,
                "allowed": allowed,
            }
        )
