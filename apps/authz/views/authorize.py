# apps/iam/views/authorize.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.access.models import Permission


class AuthorizeView(APIView):
    """
    Central IAM authorization endpoint.

    Other services call this to ask:
    'Is the authenticated user allowed to perform X?'
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        permission_code = request.data.get("permission")

        # Validate input
        if not permission_code or not isinstance(permission_code, str):
            return Response(
                {"detail": "permission is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Optional: ensure permission exists (fail fast)
        if not Permission.objects.filter(code=permission_code).exists():
            return Response(
                {"detail": "invalid permission"},
                status=status.HTTP_400_BAD_REQUEST,
            )


        # 🔐 Superadmin shortcut (CURRENT model)
        # if getattr(user, "is_superuser", False):
        #     return Response({"allowed": True})

        # Core authorization check
        allowed = request.user.has_permission(permission_code)
        
        return Response({"allowed": allowed})
