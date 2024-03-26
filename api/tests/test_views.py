from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from parameterized import parameterized
from rest_framework.test import APIClient, APITestCase

from hydroponics_manager.factories import PASSWORD, HydroponicSystemFactory, UserFactory
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
