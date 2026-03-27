from django.urls import path
from .views import ListRolesView, ListPoliciesView, ListPermissionsView

urlpatterns = [
    path('roles/', ListRolesView.as_view(), name='list-roles'),
    path('policies/', ListPoliciesView.as_view(), name='list-policies'),
    path('permissions/', ListPermissionsView.as_view(), name='list-permissions'),
]
