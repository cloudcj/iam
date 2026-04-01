from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRoleListView, ApplianceTypeView

router = DefaultRouter()
router.register(r'appliance-types',ApplianceTypeView)

urlpatterns = [
  path('user-roles/', UserRoleListView.as_view(), name='user-roles'),
  path('', include(router.urls))
]