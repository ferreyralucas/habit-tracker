from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

"""
Allows Swagger display

Args:
    Info: Swagger API Info object
    public: if True, all endpoints are included regardless of access through request
    permission_classes: permission classes for the schema view itself
"""
schema_view = get_schema_view(
    openapi.Info(
        title="Documentación de habit loop tracker ",
        default_version='v1',
        description="Documentación Pública de habit loop tracker",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls)
]
