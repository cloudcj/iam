from rest_framework import viewsets
from ..models import TransceiverType
from ..serializers import TransceiverTypeSerializer

class TransceiverTypeView(viewsets.ModelViewSet):
    queryset = TransceiverType.objects.all()
    serializer_class = TransceiverTypeSerializer
