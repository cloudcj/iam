from django.urls import path
from apps.authn.views.test import ProtectedTestView
from apps.authn.views import (
    LoginView, 
    LogoutView, 
    RefreshTokenView,
    CSRFTokenView, 
    )

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView,
# )


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("test/protected/", ProtectedTestView.as_view()),
    path("refresh/", RefreshTokenView.as_view()),
    path("csrf/", CSRFTokenView.as_view()),

    # path("api/token/", TokenObtainPairView.as_view()),
    # path("api/token/refresh/", TokenRefreshView.as_view()),
    # path("api/token/blacklist/", TokenBlacklistView.as_view()),

]
