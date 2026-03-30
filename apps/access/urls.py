from django.urls import path
from .views import ListRolesView, RoleFormOptionsView, ListPoliciesView, ListPermissionsView

urlpatterns = [
    path('roles/', ListRolesView.as_view(), name='list-roles'),
    path('roles/form-options/', RoleFormOptionsView.as_view(), name='role-form-options'),
    path('policies/', ListPoliciesView.as_view(), name='list-policies'),
    path('permissions/', ListPermissionsView.as_view(), name='list-permissions'),
]
