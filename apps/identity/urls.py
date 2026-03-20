from django.urls import path
# from .views.test import ProtectedTestView
from .views.user import (
    CreateUserView,
    # UpdateUserBasicView,
    # UpdateUserRolesView,
    # ListUsersView,
    # UpdateUserDepartmentView,
    # DeleteUserView,
    )
from apps.identity.views.me.me import MeView
from apps.identity.views.me.me_systems import MeSystemsView 

urlpatterns = [
    path("users/", CreateUserView.as_view(), name="create-user"),
    # path("users/<uuid:user_id>/basic/", UpdateUserBasicView.as_view()),
    # path("users/<uuid:user_id>/roles/", UpdateUserRolesView.as_view()),
    # path("users/list/", ListUsersView.as_view(), name="list-users"),
    # path("users/<uuid:user_id>/department/",UpdateUserDepartmentView.as_view()),
    # path("users/<uuid:user_id>/delete/",DeleteUserView.as_view()),
]

me_urlpatterns = [
    path("", MeView.as_view(), name="me"),
    path("systems/", MeSystemsView.as_view(), name="me-systems"),
]
