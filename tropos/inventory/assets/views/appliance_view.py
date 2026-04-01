from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from inventory.common.filters import ApplianceFilter

from inventory.assets.models import Appliance
from inventory.assets.serializers import (
    ApplianceSummarySerializer,
    ApplianceDetailSerializer
)
from inventory.assets.serializers import ApplianceWriteSerializer
from inventory.assets.services import ApplianceService


class ApplianceViewSet(viewsets.ModelViewSet):
    queryset = Appliance.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplianceFilter

    def get_serializer_class(self):
        """
        Use different serializers depending on action:
        - list: summary view
        - retrieve: detail view
        - create/update: write serializer
        """
        if self.action == 'list':
            return ApplianceSummarySerializer
        elif self.action in ['retrieve']:
            return ApplianceDetailSerializer
        return ApplianceWriteSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(e.detail)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(e.detail)
