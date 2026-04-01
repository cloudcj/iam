from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Building
from ..serializers import BuildingSerializer
from inventory.common.mixins import AuditLogMixin, SuccessMessageMixin
from inventory.common.filters import BuildingFilter

class BuildingViewSet(AuditLogMixin,SuccessMessageMixin, viewsets.ModelViewSet):
  queryset = Building.objects.all()
  serializer_class = BuildingSerializer  
  pagination_class = None

  filter_backends = [DjangoFilterBackend]
  filterset_class = BuildingFilter
