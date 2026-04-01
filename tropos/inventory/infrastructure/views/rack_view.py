from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from inventory.common.pagination import CustomPagination
from inventory.common.mixins import PatchOnlyModelMixin, AuditLogMixin,SuccessMessageMixin

from ..models import Rack, RackPosition
from ..serializers import RackSerializer, RackPositionSerializer


class RackViewSet(AuditLogMixin,SuccessMessageMixin, viewsets.ModelViewSet):
  queryset = Rack.objects.all()
  serializer_class = RackSerializer
  filterset_fields = ['is_occupied', 'environment']

class RackPositionViewSet(
  ListModelMixin, 
  RetrieveModelMixin, 
  PatchOnlyModelMixin,
  AuditLogMixin,
  viewsets.GenericViewSet
  ):
  queryset = RackPosition.objects.all()
  serializer_class = RackPositionSerializer
  pagination_class = CustomPagination
  filterset_fields = ['rack', 'position_number', 'is_occupied', 'device']