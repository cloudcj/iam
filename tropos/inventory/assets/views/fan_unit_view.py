from rest_framework import viewsets
from ..models import FanUnit
from inventory.assets.serializers import (
    FanUnitSerializer,
    ShowAllFanUnitSerializer
)

class FanUnitViewSet(viewsets.ModelViewSet):
    queryset = FanUnit.objects.all()

    def get_serializer_class(self):
        # Use summary serializer for list; full details for retrieve/create/update
        if self.action == 'list':
            return FanUnitSerializer
        return ShowAllFanUnitSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        device_id = self.request.query_params.get("device_id")
        pkid = self.request.query_params.get("pkid")

        if device_id:
            queryset = queryset.filter(device_id=device_id)
        if pkid:
            queryset = queryset.filter(id=pkid)

        return queryset
