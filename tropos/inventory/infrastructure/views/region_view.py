from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from ..models import Region
from ..serializers import RegionSerializer
from inventory.common.mixins import AuditLogMixin,SuccessMessageMixin

class RegionViewSet(AuditLogMixin, SuccessMessageMixin, viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = None

    filter_backends = [filters.SearchFilter]

    search_fields = ["id", "name"]

    # create_message = "Region created successfully."
    # update_message = "Region updated successfully."
    # delete_message = "Region deleted successfully."