from rest_framework import viewsets

from inventory.common.mixins import AuditLogMixin, SuccessMessageMixin
from ..models import Room
from ..serializers import RoomSerializer

class RoomViewSet(AuditLogMixin,SuccessMessageMixin, viewsets.ModelViewSet):
  queryset = Room.objects.all()
  serializer_class = RoomSerializer
  pagination_class = None