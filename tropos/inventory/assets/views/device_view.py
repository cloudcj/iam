from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from inventory.assets.models import Device
from inventory.assets.serializers import DeviceSerializer
from inventory.common.pagination import CustomPagination
from inventory.common.filters import DeviceFilter

# class DeviceViewSet(
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet
# ):  

class DeviceViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DeviceFilter

    # 👇 Allow only safe fields for ordering
    ordering_fields = ['type', 'created_at', 'updated_at', 'number_of_interfaces']
    ordering = ['-created_at']  # 👈 Default sorting (newest first)

    def get_queryset(self):
        return Device.non_decommissioned.visible() \
            .prefetch_related('interfaces', 'rack_positions') \
            .annotate(number_of_interfaces=Count('interfaces'))

    # def get_queryset(self):
    #     return Device.objects.all() \
    #         .prefetch_related('interfaces', 'rack_positions') \
    #         .annotate(number_of_interfaces=Count('interfaces'))
