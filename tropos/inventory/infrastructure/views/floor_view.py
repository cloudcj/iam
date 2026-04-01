from rest_framework import viewsets

from ..models import Floor
from ..serializers import FloorSerializer
from inventory.common.mixins import AuditLogMixin, SuccessMessageMixin

class FloorViewSet(AuditLogMixin,SuccessMessageMixin, viewsets.ModelViewSet):
  queryset = Floor.objects.all()
  serializer_class = FloorSerializer
  pagination_class = None