from rest_framework import viewsets

from ..models import Pod
from ..serializers import PodSerializer
from inventory.common.mixins import AuditLogMixin, SuccessMessageMixin

class PodViewSet(AuditLogMixin,SuccessMessageMixin, viewsets.ModelViewSet):
  queryset = Pod.objects.all()
  serializer_class = PodSerializer
  pagination_class = None