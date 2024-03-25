"""
    Factory for:
        - User model
        - HydroponicSystem model
        - Measurement model
"""
from django.contrib.auth.models import User
from factory import PostGenerationMethodCall, Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import HydroponicSystem, Measurement

FAKER = Faker()
PASSWORD = "1_test_TEST_!"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user_{n}")
    password = PostGenerationMethodCall("set_password", PASSWORD)


class HydroponicSystemFactory(DjangoModelFactory):
    class Meta:
        model = HydroponicSystem

    owner = SubFactory(UserFactory)
    name = Sequence(lambda n: f"name_{n}")


class MeasurementFactory(DjangoModelFactory):
    class Meta:
        model = Measurement

    hydroponic_system = SubFactory(HydroponicSystemFactory)
