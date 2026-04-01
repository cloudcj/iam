from rest_framework import viewsets
from ..models import Interface
from inventory.assets.serializers import InterfaceDetailSerializer
from rest_framework.pagination import PageNumberPagination

class InterfacePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 48

class InterfaceViewSet(viewsets.ModelViewSet):
    serializer_class = InterfaceDetailSerializer
    queryset = Interface.objects.all()  # ← required for router
    pagination_class = InterfacePagination

    def get_queryset(self):
        queryset = super().get_queryset()
        device_id = self.request.query_params.get("device_id")
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        return queryset

