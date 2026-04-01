# views/server_view.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Server,Device
from ..serializers import (
    ServerSummarySerializer,
    ServerDetailSerializer,
    ServerWriteSerializer,
)
from inventory.common.filters import ServerFilter
from inventory.assets.services import ServerService
from inventory.common.mixins import AuditLogMixin

class ServerViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing servers.
    - GET /servers/ → ServerSummarySerializer
    - GET /servers/<id>/ → ServerDetailSerializer
    - POST/PUT/PATCH → ServerWriteSerializer
    - DELETE → soft delete server via ServerService
    """
    # queryset = Server.objects.select_related('device').all()  # include all servers
    queryset = Server.objects.filter(device__in=Device.non_decommissioned.visible())
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServerFilter
    def get_queryset(self):
        """
        Return all servers, optionally filtered by query params: device_id, rack_id, name.
        This includes decommissioned servers.
        """
        queryset = self.queryset
        params = self.request.query_params

        device_id = params.get("device.id") or params.get("device_id")
        rack_id = params.get("rack_id")
        name = params.get("name")

        if device_id:
            queryset = queryset.filter(device__id=device_id)
        if rack_id:
            queryset = queryset.filter(device__rack_id=rack_id)
        if name:
            queryset = queryset.filter(server_name__icontains=name)

        return queryset

    def get_serializer_class(self):
        """
        Dynamically choose serializer based on action and result count.
        """
        if self.action == "list":
            return ServerSummarySerializer
        elif self.action == "retrieve":
            return ServerDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ServerWriteSerializer

        queryset = self.filter_queryset(self.get_queryset())
        if queryset.count() == 1:
            return ServerDetailSerializer

        return ServerSummarySerializer

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete a server using ServerService.
        """
        instance = self.get_object()
        ServerService.retire_server(instance)
        return Response(
            {"message": "Server successfully decommissioned."},
            status=status.HTTP_200_OK,
        )
