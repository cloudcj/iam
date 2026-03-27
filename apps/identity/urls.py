# from django.urls import path
# # from .views.test import ProtectedTestView
# from .views.user import (
#     CreateUserView,
#     # UpdateUserBasicView,
#     # UpdateUserRolesView,
#     # ListUsersView,
#     # UpdateUserDepartmentView,
#     # DeleteUserView,
#     )
# from apps.identity.views.me.me import MeView
# from apps.identity.views.me.me_systems import MeSystemsView 

# urlpatterns = [
#     path("users/", CreateUserView.as_view(), name="create-user"),
#     # path("users/<uuid:user_id>/basic/", UpdateUserBasicView.as_view()),
#     # path("users/<uuid:user_id>/roles/", UpdateUserRolesView.as_view()),
#     # path("users/list/", ListUsersView.as_view(), name="list-users"),
#     # path("users/<uuid:user_id>/department/",UpdateUserDepartmentView.as_view()),
#     # path("users/<uuid:user_id>/delete/",DeleteUserView.as_view()),
# ]

# me_urlpatterns = [
#     path("", MeView.as_view(), name="me"),
#     path("systems/", MeSystemsView.as_view(), name="me-systems"),
# ]

from django.urls import path
# from .views.test import ProtectedTestView
from .views.user import (
    CreateUserView,
    ListUsersView,
    UpdateUserFullView,
    DeleteUserView,
    UserDetailView,
    ResetUserPasswordView,
)
from apps.identity.views.me import MeView, UpdateProfileView, ChangePasswordView

urlpatterns = [
    path("users/", ListUsersView.as_view(), name="list-users"),
    path("users/create/", CreateUserView.as_view(), name="create-user"),
    path("users/<uuid:user_id>/update/", UpdateUserFullView.as_view(), name="update-user"),
    path("users/<uuid:user_id>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<uuid:user_id>/delete/", DeleteUserView.as_view()),

    path("users/<uuid:user_id>/reset-password/", ResetUserPasswordView.as_view()),
]

me_urlpatterns = [
    path("", MeView.as_view(), name="me"),
    path("profile/", UpdateProfileView.as_view(), name="me-update-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="me-change-password"),
]
