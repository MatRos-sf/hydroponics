from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class HydroponicSystem(models.Model):
    """
    Model presents hydroponic system
    """

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="systems")
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Measurement(models.Model):
    measurement_date = models.DateTimeField(auto_now_add=True)
    ph = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(14)],
    )
    water_temperature = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Water temperature is measured in degrees Celsius",
    )
    tds = models.FloatField(
        blank=True, null=True, help_text="TDS is present in mg/L units"
    )
    hydroponic_system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="measurements"
    )
