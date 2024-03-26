from http import HTTPStatus
from random import uniform

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from parameterized import parameterized
from rest_framework.test import APIClient, APITestCase

from hydroponics_manager.factories import (
    PASSWORD,
    ExtendedMeasurementFactory,
    HydroponicSystemFactory,
    MeasurementFactory,
    UserFactory,
)
from hydroponics_manager.models import HydroponicSystem, Measurement


@tag("hs")
class HydroponicSystemListAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(HydroponicSystemListAPIViewTest, cls).setUpClass()
        users = UserFactory.create_batch(2)

        for user in users:
            HydroponicSystemFactory.create_batch(10, owner=user)

    def setUp(self):
        self.user = User.objects.first()
        self.url = reverse("api:list")

    def test_should_create_20_hydroponic_systems(self):
        self.assertEqual(HydroponicSystem.objects.count(), 20)

    def test_user_should_have_10_hydroponic_systems(self):
        self.assertEqual(HydroponicSystem.objects.filter(owner=self.user).count(), 10)

    def test_should_return_status_code_forbidden_when_did_not_provide_credentials(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_should_return_status_code_ok_for_authenticated_user(self):
        credentials = {"username": self.user.username, "password": PASSWORD}
        self.client.login(**credentials)
        response = self.client.get(self.url, data=credentials)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_10_hydroponic_systems(self):
        credentials = {"username": self.user.username, "password": PASSWORD}
        self.client.login(**credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        data = response.json()
        self.assertEqual(len(data), 10)


@tag("ms")
class MeasurementListAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(MeasurementListAPIViewTest, cls).setUpClass()
        users = UserFactory.create_batch(2)

        # first user -> 2hs, 20 random measurement
        first_user = users[0]
        list_of_hs = HydroponicSystemFactory.create_batch(2, owner=first_user)
        for index, hs in enumerate(list_of_hs):
            if index == 0:
                ExtendedMeasurementFactory.create_batch(15, hydroponic_system=hs)
            else:
                ExtendedMeasurementFactory.create_batch(5, hydroponic_system=hs)

        # second user
        second_user = users[-1]
        hs = HydroponicSystemFactory(owner=second_user)
        ExtendedMeasurementFactory.create_batch(15, hydroponic_system=hs)

    def setUp(self):
        self.user = User.objects.first()
        self.url = "api:measurement-list"

    def test_should_create_20_measurement_for_main_user(self):
        hs_first, hs_second = HydroponicSystem.objects.filter(owner=self.user)
        self.assertEqual(
            Measurement.objects.filter(hydroponic_system=hs_first).count(), 15
        )
        self.assertEqual(
            Measurement.objects.filter(hydroponic_system=hs_second).count(), 5
        )

    def test_should_return_status_code_forbidden_when_user_did_not_provide_credentials(
        self,
    ):
        hs = HydroponicSystem.objects.filter(owner=self.user).first()
        url = reverse("api:measurement-list", kwargs={"pk": hs.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_should_return_ten_last_measurement(self):
        hs = HydroponicSystem.objects.filter(owner=self.user).first()
        url = reverse("api:measurement-list", kwargs={"pk": hs.pk})

        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()["data"]), 10)
