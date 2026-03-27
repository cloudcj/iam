from django.urls import path
from .views import ListDepartmentsView, CreateDepartmentView, UpdateDepartmentView, DeleteDepartmentView

urlpatterns = [
    path('', ListDepartmentsView.as_view(), name='list-departments'),
    path('create/', CreateDepartmentView.as_view(), name='create-department'),
    path('<uuid:department_id>/update/', UpdateDepartmentView.as_view(), name='update-department'),
    path('<uuid:department_id>/delete/', DeleteDepartmentView.as_view(), name='delete-department'),
]
