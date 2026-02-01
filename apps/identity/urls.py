from django.urls import path
# from .views.test import ProtectedTestView
from .views.user import (
    CreateUserView,
    UpdateUserInfoView,
    UpdateUserRolesView,
    ListUsersView,
    UpdateUserDepartmentView,
    DeleteUserView
    )

urlpatterns = [
    path("users/", CreateUserView.as_view(), name="create-user"),
    path("users/<uuid:user_id>/", UpdateUserInfoView.as_view()),
    path("users/<uuid:user_id>/roles/", UpdateUserRolesView.as_view()),
    path("users/list/", ListUsersView.as_view(), name="list-users"),
    path("users/<uuid:user_id>/department/",UpdateUserDepartmentView.as_view()),
    path("users/<uuid:user_id>/delete/",DeleteUserView.as_view()),

]
