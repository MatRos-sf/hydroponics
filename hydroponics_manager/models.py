from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet


class HydroponicsType(models.TextChoices):
    # https://www.wiki.haszysz.com/index.php/Rodzaje_system%C3%B3w_hydroponicznych
    AEROPONIC = "AEROPONIC", "Aeroponic Systems"
    DRIPPER_FEED = "DRIPPER_FEED", "Dripper Feed Systems"
    EBB_AND_FLOOD = "EBB_AND_FLOOD", "Ebb & Flood System"
    NFT = "NFT", "Nutrient Film Technique"
    POT = "POT", "POT CULTURE"


class HydroponicSystem(models.Model):
    """
    Model presents hydroponic system
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="systems")

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    system_type = models.CharField(
        max_length=50,
        choices=HydroponicsType.choices,
        help_text="Type of hydroponic system",
    )

    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    water_capacity = models.FloatField(blank=True, null=True)

    # I could add fields for example: water_refill_interval, nutrient_refill_interval, pump_runtime_daily
    class Meta:
        ordering = ("-created",)
        # unique_together = ("owner", "name")

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("hydroponic_system:detail", kwargs={"pk": self.pk})

    def last_measurements(self) -> QuerySet:
        return self.measurements.all().values(
            "timestamp", "ph", "water_temperature", "tds"
        )[:10]


class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ph = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(14.0)],
    )
    water_temperature = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Water temperature is measured in degrees Celsius",
    )
    tds = models.FloatField(
        blank=True, null=True, help_text="TDS is present in mg/L units"
    )
    hydroponic_system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="measurements"
    )

    class Meta:
        ordering = ["-timestamp"]

    def save(self, *args, **kwargs) -> None:
        if self.ph and not (0 <= self.ph <= 14):
            raise ValidationError({"ph": "pH value must be between 0 and 14"})

        if self.water_temperature and not (0 <= self.water_temperature <= 100):
            raise ValidationError(
                {"water_temperature": "The water temperature must be between 0 and 100"}
            )

        super(Measurement, self).save()
