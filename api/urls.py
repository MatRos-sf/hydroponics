from django.urls import path

from .views import (
    HydroponicSystemListAPIView,
    MeasurementCreateAPIView,
    MeasurementListAPIView,
)

app_name = "api"

urlpatterns = [
    path("", MeasurementCreateAPIView.as_view(), name="send-measurement"),
    path("hydroponics/", HydroponicSystemListAPIView.as_view(), name="list"),
    path(
        "measurements/<int:pk>/",
        MeasurementListAPIView.as_view(),
        name="measurement-list",
    ),
]
