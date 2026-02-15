# # identity/views/me_view.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from django.contrib.auth import get_user_model

# from apps.identity.serializers.user import MeSerializer

# User = get_user_model()

# class MeView(APIView):
#     def get(self, request):
#         user = (
#             User.objects
#             .prefetch_related(
#                 "user_roles__role",
#                 "user_department__department",
#             )
#             .get(pk=request.user.pk)
#         )

#         serializer = MeSerializer(user)
#         return Response(serializer.data)


# apps/identity/views/me.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...serializers.user import MeSerializer


# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = MeSerializer(request.user)
#         return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authz.service.authorization_service import AuthorizationService
from ...serializers.user import MeSerializer



class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1️⃣ Resolve permissions (cached per request)
        permission_codes = AuthorizationService.get_user_permission_codes(user)

        # 2️⃣ Group permissions by system
        grouped_permissions = AuthorizationService.group_permissions_by_system(
            permission_codes
        )

        # 3️⃣ Derive systems from grouped permissions
        systems = [
            {
                "code": system,
                "label": system.upper(),  # replace with registry if needed
            }
            for system in sorted(grouped_permissions.keys())
        ]

        # 4️⃣ Build projection explicitly
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "department": {
                "code": user.department.code,
                "label": user.department.name,
            },
            "systems": systems,
            "permissions": grouped_permissions,
        }

        # 5️⃣ Serialize projection
        serializer = MeSerializer(data)

        return Response(serializer.data)


# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         permission_codes = AuthorizationService.get_user_permission_codes(user)

#         grouped_permissions = AuthorizationService.group_permissions_by_system(
#             permission_codes
#         )
#         systems = [
#             {
#                 "code": system,
#                 "label": system.upper(),
#             }
#             for system in sorted(grouped_permissions.keys())
#         ]

#         serializer = MeSerializer(
#             user,
#             context={
#                 "systems": systems,
#                 "permissions": grouped_permissions,
#             }
#         )

#         return Response(serializer.data)
