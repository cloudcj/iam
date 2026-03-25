from django.urls import path
from .views import ListDepartmentsView

urlpatterns = [
    path('departments/', ListDepartmentsView.as_view(), name='list-departments'),
]
