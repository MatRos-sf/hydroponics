from django import forms

from .models import HydroponicSystem


class HydroponicSystemForm(forms.ModelForm):
    class Meta:
        model = HydroponicSystem
        fields = ("name", "description", "system_type", "water_capacity")
