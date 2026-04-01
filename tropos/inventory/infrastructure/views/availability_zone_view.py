from rest_framework import viewsets
from inventory.common.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend

from ..models import AvailabilityZone
from ..serializers import AZSerializer
from inventory.common.mixins import AuditLogMixin, SuccessMessageMixin
from inventory.common.filters import AvailabilityZoneFilter

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

@method_decorator(ensure_csrf_cookie, name='dispatch')
class AZViewSet(AuditLogMixin,SuccessMessageMixin, viewsets.ModelViewSet):
  queryset = AvailabilityZone.objects.all() #.order_by('id') - this is if you want to add pagination and be in order
  serializer_class = AZSerializer
  pagination_class =  None     #CustomPagination
  filter_backends = [DjangoFilterBackend]
  filterset_class = AvailabilityZoneFilter
