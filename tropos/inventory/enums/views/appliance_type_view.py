from rest_framework import viewsets
from ..models.appliance_type_enums import ApplianceType
from ..serializers.appliance_type_serializer import ApplianceTypeSerializer

class ApplianceTypeView(viewsets.ModelViewSet):
    queryset = ApplianceType.objects.all()
    serializer_class = ApplianceTypeSerializer
