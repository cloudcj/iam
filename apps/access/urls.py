from django.urls import path
from .views import ListRolesView

urlpatterns = [
    path('roles/', ListRolesView.as_view(), name='list-roles'),
]
