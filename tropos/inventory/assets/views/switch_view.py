
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Device,Switch
from inventory.assets.serializers import SwitchSummarySerializer
from inventory.assets.serializers  import SwitchWriteSerializer
from inventory.assets.services import SwitchService 
from inventory.common.mixins import AuditLogMixin

from inventory.assets.serializers.devices import DeviceSerializer
from inventory.common.filters import SwitchFilter


class SwitchViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    ViewSet for Switches, backed by the Switch model, but filtered by Device attributes.
    """
    # queryset = Switch.non_decommissioned.visible().filter(type="switch")
    # queryset = Switch.objects.all()
    # queryset = device.switch.objects.filter(device__in=Device.non_decommissioned.visible())
    # queryset = Device.non_decommissioned.visible().filter(type="switch")
    queryset = Switch.objects.filter(device__in=Device.non_decommissioned.visible())

    filter_backends = [DjangoFilterBackend]
    filterset_class = SwitchFilter



    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SwitchSummarySerializer
        return SwitchWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use SwitchService to create the Switch
        switch = serializer.save()  

        # Serialize the created object for the response
        response_serializer = self.get_serializer(switch)
        return Response(
            {
                "message": "Switch created successfully.",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: delegate to SwitchService
        """
        instance = self.get_object()
        SwitchService.retire_switch(instance)  # centralized soft delete
        return Response(
            {"message": "Switch successfully deleted."},
            status=status.HTTP_200_OK
        )
