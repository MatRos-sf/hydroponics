from django.contrib.auth.models import User
from django.test import TestCase, tag

from .factories import HydroponicSystemFactory, MeasurementFactory, UserFactory
from .models import HydroponicSystem, Measurement


class HydroponicSystemTest(TestCase):
    @classmethod
    def setUpClass(cls):
        UserFactory.create_batch(3)

    def test_should_create_3_users(self):
        self.assertEqual(User.objects.count(), 3)

    def test_should_create_3_hydroponicsystems(self):
        HydroponicSystemFactory.create_batch(3)
        self.assertEqual(HydroponicSystem.objects.count(), 3)
