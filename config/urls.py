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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from apps.identity.urls import me_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView



urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication (public entry)
    path("api/v1/auth/", include("apps.authn.urls")),

    # Identity management (users, roles, orgs)
    path("api/v1/identity/", include("apps.identity.urls")),

    # Self-scoped identity
    path("api/v1/me/", include(me_urlpatterns)),

    # Departments
    path("api/v1/department/", include("apps.department.urls")),

    # Roles
    path("api/v1/access/", include("apps.access.urls")),

    #
    path("api/v1/audit/", include("apps.audit.urls")),

    # Dashboard
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]




# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("api/auth/", include("apps.authn.urls")),
#     path("api/identity/", include("apps.identity.urls")),

#     path("api/v1/me/", MeView.as_view(), name="me"),
#     path("api/v1/me/systems", MeSystemsView.as_view(), name="me-systems"),

#     # path("api/.well-known/jwks.json", jwks_view),
#     path("api/iam/", include("apps.authz.urls")),
# ]