from rest_framework.generics import CreateAPIView

from hydroponics_manager.models import Measurement

from .serializers import MeasurementSerializer


class MeasurementCreateAPIView(CreateAPIView):
    model = Measurement
    serializer_class = MeasurementSerializer
