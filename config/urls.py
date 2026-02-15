"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# from apps.services.jwks import jwks_view
from apps.identity.views.me.me import MeView
from apps.identity.views.me.me_systems import MeSystemsView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("apps.authn.urls")),
    path("api/identity/", include("apps.identity.urls")),

    path("api/v1/me/", MeView.as_view(), name="me"),
    path("api/v1/me/systems", MeSystemsView.as_view(), name="me-systems"),

    # path("api/.well-known/jwks.json", jwks_view),
    path("api/iam/", include("apps.authz.urls")),
]