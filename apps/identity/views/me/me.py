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


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
