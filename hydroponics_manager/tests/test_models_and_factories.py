from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from parameterized import parameterized

from hydroponics_manager.factories import (
    HydroponicSystemFactory,
    MeasurementFactory,
    UserFactory,
)
from hydroponics_manager.models import HydroponicSystem, Measurement


class FactoriesSimpleTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(FactoriesSimpleTest, cls).setUpClass()
        UserFactory.create_batch(3)

    def test_should_create_3_users(self):
        self.assertEqual(User.objects.count(), 3)

    def test_should_create_3_hydroponicsystems(self):
        for user in User.objects.all():
            HydroponicSystemFactory(owner=user)

        self.assertEqual(HydroponicSystem.objects.count(), 3)

    def test_should_create_3_measurements(self):
        for user in User.objects.all():
            hs = HydroponicSystemFactory(owner=user)
            MeasurementFactory(hydroponic_system=hs)

        self.assertEqual(Measurement.objects.count(), 3)


class MeasurementsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.hs = HydroponicSystemFactory(owner=self.user)

    @parameterized.expand([0, 0.1, 5, 5.555, 14.0, 13.99])
    def test_should_set_ph_when_is_correct(self, ph):
        instance = MeasurementFactory(hydroponic_system=self.hs, ph=ph)
        self.assertEqual(instance.ph, ph)

    @parameterized.expand([-0.001, -0.1, -5, -14, 14.1, 152])
    def test_when_ph_is_out_of_range_should_return_exception(self, ph):
        with self.assertRaises(ValidationError):
            MeasurementFactory(hydroponic_system=self.hs, ph=ph)

    @parameterized.expand([0, 0.1, 50, 100])
    def test_should_set_water_temperature_when_is_correct(self, temp):
        instance = MeasurementFactory(hydroponic_system=self.hs, water_temperature=temp)
        self.assertEqual(instance.water_temperature, temp)

    @parameterized.expand([-0.1, -5, 100.1, 251])
    def test_when_water_temperature_is_out_of_range_should_return_exception(self, temp):
        with self.assertRaises(ValidationError):
            MeasurementFactory(hydroponic_system=self.hs, water_temperature=temp)

    def test_should_set_none_value_when_water_temperature_and_ph_are_not_provided(self):
        measurement = MeasurementFactory(hydroponic_system=self.hs)
        self.assertIsNone(measurement.water_temperature)
        self.assertIsNone(measurement.ph)
        self.assertIsNone(measurement.tds)
