from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


class MeasurementListAPIView(ListAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Measurement.objects.filter(
            hydroponic_system__pk=self.kwargs.get("pk"),
            hydroponic_system__owner=self.request.user,
        )[:10]

    def list(self, request, *args, **kwargs) -> Response:
        super(MeasurementListAPIView, self).list(request, *args, **kwargs)
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        hs = HydroponicSystem.objects.get(pk=self.kwargs.get("pk"))
        response_data = {"name": hs.name, "data": serializer.data}

        return Response(response_data)
