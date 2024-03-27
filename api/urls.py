from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    HydroponicSystemListAPIView,
    HydroponicSystemRetrieveUpdateDestroyAPIView,
    MeasurementCreateAPIView,
    MeasurementListAPIView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Hydroponics",
        default_version="v1",
        description="Interview",
        contact=openapi.Contact(email="mateuszrosenkranz@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "api"

urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", MeasurementCreateAPIView.as_view(), name="send-measurement"),
    path(
        "hydroponics/",
        include(
            [
                path("", HydroponicSystemListAPIView.as_view(), name="list"),
                path(
                    "<int:pk>/",
                    HydroponicSystemRetrieveUpdateDestroyAPIView.as_view(),
                    name="rud-hydroponic-system",
                ),
            ]
        ),
    ),
    path(
        "measurements/<int:pk>/",
        MeasurementListAPIView.as_view(),
        name="measurement-list",
    ),
]
