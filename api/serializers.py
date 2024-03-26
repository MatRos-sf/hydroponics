from typing import Any, Dict

from rest_framework import serializers

from hydroponics_manager.models import HydroponicSystem, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ("ph", "water_temperature", "tds", "hydroponic_system")


class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        exclude = ("owner",)

    def to_representation(self, instance) -> Dict[Any, Any | None]:
        data = super(HydroponicSystemSerializer, self).to_representation(instance)
        data["system_type"] = instance.get_system_type_display()
        data["created"] = instance.created.strftime("%Y-%m-%d %H:%M:%S")
        return data
