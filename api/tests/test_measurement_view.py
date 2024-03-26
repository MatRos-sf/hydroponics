from http import HTTPStatus

from django.test import tag
from django.urls import reverse
from parameterized import parameterized
from rest_framework.test import APIClient, APITestCase

from hydroponics_manager.factories import HydroponicSystemFactory, UserFactory
from hydroponics_manager.models import HydroponicSystem, Measurement


@tag("api_sensor")
class SensorTests(APITestCase):
    """
    Tests simulate a sensor by sending POST requests to the API View
    """

    def setUp(self):
        user = UserFactory()
        HydroponicSystemFactory(owner=user)
        self.url = reverse("api:send-measurement")

    @parameterized.expand(
        [
            ({"ph": 6, "water_temperature": 15, "tds": 10, "hydroponic_system": 1},),
            ({"water_temperature": 15, "tds": 10, "hydroponic_system": 1},),
            ({"tds": 10, "hydroponic_system": 1},),
            ({"hydroponic_system": 1},),
        ]
    )
    def test_should_send_and_create_measurement(self, data):
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Measurement.objects.count(), 1)

    @parameterized.expand([0, 3, 42, -1])
    def test_should_status_code_400_when_hydroponic_system_does_not_exist(self, hs_pk):
        data = {"ph": 6, "water_temperature": 15, "tds": 10, "hydroponic_system": hs_pk}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand(["put", "get", "delete"])
    def test_should_return_method_not_allowed(self, method):
        data = {"ph": 6, "water_temperature": 15, "tds": 10, "hydroponic_system": 1}
        response = getattr(self.client, method)(self.url, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
