from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeviceViewSet,
    SwitchViewSet,
    ApplianceViewSet,
    PowerSupplyUnitViewSet,
    InterfaceViewSet,
    ServerViewSet,
    FanUnitViewSet,
    # AssetsLookupView
)

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'switches', SwitchViewSet)
router.register(r'servers', ServerViewSet)
router.register(r'appliances', ApplianceViewSet)
router.register(r'interfaces', InterfaceViewSet)
router.register(r'power_supply_units', PowerSupplyUnitViewSet)
router.register(r'fan_units', FanUnitViewSet)


# Combine router URLs + generic lookup
urlpatterns = [
    path("", include(router.urls)),  # main CRUD endpoints
    # path("lookups/<str:model_name>/", AssetsLookupView.as_view(), name="generic-lookup"),  # generic dropdown API
]

