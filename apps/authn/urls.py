from django.urls import path
from apps.authn.views.test import ProtectedTestView
from apps.authn.views import (
    LoginView, 
    LogoutView, 
    RefreshTokenView,
    CSRFTokenView, 
    # CreateUserView,
    # UpdateUserIdentityView,
    # UpdateUserRolesView,
    # ListUsersView,
    # UpdateUserDepartmentView
    )

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("test/protected/", ProtectedTestView.as_view()),
    path("refresh/", RefreshTokenView.as_view()),
    path("csrf/", CSRFTokenView.as_view()),
    # path("users/", CreateUserView.as_view(), name="create-user"),
    # path("users/<uuid:user_id>/", UpdateUserIdentityView.as_view()),
    # path("users/<uuid:user_id>/roles/", UpdateUserRolesView.as_view()),
    # path("users/list/", ListUsersView.as_view(), name="list-users"),
    # path("users/<uuid:user_id>/department/",UpdateUserDepartmentView.as_view()),

]
