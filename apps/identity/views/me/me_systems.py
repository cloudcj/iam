from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.access.services.me.system_visibility import (
    get_visible_systems_for_user,
)


class MeSystemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        systems = get_visible_systems_for_user(request.user)

        return Response(
            {
                "systems": [
                    {
                        "code": system,
                        "label": system.capitalize(),
                    }
                    for system in systems
                ]
            }
        )
