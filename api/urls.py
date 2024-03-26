from django.urls import path

from .views import MeasurementCreateAPIView

app_name = "api"

urlpatterns = [path("", MeasurementCreateAPIView.as_view(), name="send-measurement")]
