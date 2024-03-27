from django.urls import include, path

from .views import (
    HydroponicSystemListAPIView,
    HydroponicSystemRetrieveUpdateDestroyAPIView,
    MeasurementCreateAPIView,
    MeasurementListAPIView,
)

app_name = "api"

urlpatterns = [
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
