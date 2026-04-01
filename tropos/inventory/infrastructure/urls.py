from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet,
    AZViewSet, 
    BuildingViewSet, 
    FloorViewSet, 
    RoomViewSet, 
    PodViewSet, 
    RackViewSet, 
    RackPositionViewSet, 
    PowerDeliveryUnitViewSet, 
    PowerDeliveryUnitOutletViewSet,
    InfraLookupView
)

# Main router for CRUD endpoints
router = DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'availability-zones', AZViewSet)
router.register(r'buildings', BuildingViewSet)
router.register(r'floors', FloorViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'pods', PodViewSet)
router.register(r'racks', RackViewSet)
router.register(r'rack-positions', RackPositionViewSet)
router.register(r'pdus', PowerDeliveryUnitViewSet)
router.register(r'pdu-outlets', PowerDeliveryUnitOutletViewSet)

# Combine router URLs + generic lookup
urlpatterns = [
    path("", include(router.urls)),  # main CRUD endpoints
    path("lookups/<str:model_name>/", InfraLookupView.as_view(), name="generic-lookup"),  # generic dropdown API
]
