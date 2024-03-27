from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import HydroponicSystem


class HydroponicSystemForm(forms.ModelForm):
    class Meta:
        model = HydroponicSystem
        fields = ("name", "description", "system_type", "water_capacity")


class CustomCreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self) -> Any | None:
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email
