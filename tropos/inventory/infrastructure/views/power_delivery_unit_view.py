from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from inventory.common.mixins import PatchOnlyModelMixin, AuditLogMixin,SuccessMessageMixin

from ..models import PowerDeliveryUnit, PowerDeliveryUnitOutlet
from ..serializers import PowerDeliveryUnitSerializer, PowerDeliveryUnitOutletSerializer

class PowerDeliveryUnitViewSet(
  PatchOnlyModelMixin, 
  ListModelMixin, 
  RetrieveModelMixin,
  AuditLogMixin, SuccessMessageMixin,
  viewsets.GenericViewSet
  ):
  queryset = PowerDeliveryUnit.objects.all()
  serializer_class = PowerDeliveryUnitSerializer

class PowerDeliveryUnitOutletViewSet(AuditLogMixin, viewsets.ModelViewSet):
  queryset = PowerDeliveryUnitOutlet.objects.all()
  serializer_class = PowerDeliveryUnitOutletSerializer