from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from hydroponics_manager.models import HydroponicSystem, Measurement

from .serializers import HydroponicSystemSerializer, MeasurementSerializer


class MeasurementCreateAPIView(CreateAPIView):
    model = Measurement
    serializer_class = MeasurementSerializer


class HydroponicSystemListAPIView(ListAPIView):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)
