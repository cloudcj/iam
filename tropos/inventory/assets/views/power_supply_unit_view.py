from rest_framework import viewsets
from ..models import PowerSupplyUnit
from inventory.assets.serializers import PowerSupplyUnitSerializer, ShowAllPowerSupplyUnitSerializer

class PowerSupplyUnitViewSet(viewsets.ModelViewSet):
    queryset = PowerSupplyUnit.objects.all()

    def get_serializer_class(self):
        # Use full-detail serializer for list, simpler serializer otherwise
        if self.action == 'list':
            return PowerSupplyUnitSerializer
        return ShowAllPowerSupplyUnitSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        device_id = self.request.query_params.get("device_id")
        pkid = self.request.query_params.get("pkid")
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        if pkid:
            queryset = queryset.filter(id=pkid)
        return queryset
