from rest_framework import serializers

from hydroponics_manager.models import Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ("ph", "water_temperature", "tds", "hydroponic_system")
