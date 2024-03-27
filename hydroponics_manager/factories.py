"""
    Factory for:
        - User model
        - HydroponicSystem model
        - Measurement model
"""
from random import uniform

from django.contrib.auth.models import User
from factory import PostGenerationMethodCall, Sequence, SubFactory, post_generation
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


class ExtendedMeasurementFactory(MeasurementFactory):
    class Meta:
        model = Measurement

    hydroponic_system = SubFactory(HydroponicSystemFactory)
    ph = round(uniform(0, 14), 1)
    water_temperature = round(uniform(0, 100), 2)
    tds = round(uniform(0, 100), 2)
