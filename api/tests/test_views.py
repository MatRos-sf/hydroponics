from functools import partial
from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase

from hydroponics_manager.factories import (
    PASSWORD,
    ExtendedMeasurementFactory,
    HydroponicSystemFactory,
    UserFactory,
)
from hydroponics_manager.models import HydroponicsType, HydroponicSystem, Measurement


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
        for _ in range(15):
            ExtendedMeasurementFactory(hydroponic_system=list_of_hs[0])

        for _ in range(5):
            ExtendedMeasurementFactory(hydroponic_system=list_of_hs[1])

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
            Measurement.objects.filter(hydroponic_system=hs_first).count(), 5
        )
        self.assertEqual(
            Measurement.objects.filter(hydroponic_system=hs_second).count(), 15
        )

    def test_should_return_status_code_forbidden_when_user_did_not_provide_credentials(
        self,
    ):
        hs = HydroponicSystem.objects.filter(owner=self.user).first()
        url = reverse("api:measurement-list", kwargs={"pk": hs.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_should_return_appropriate__measurements(self):
        hs = HydroponicSystem.objects.filter(owner=self.user).all()
        hs_len = 10 if hs[0].measurements.count() > 10 else hs[0].measurements.count()

        url = reverse("api:measurement-list", kwargs={"pk": hs[0].pk})

        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()["data"]), hs_len)

        hs_len = 10 if hs[1].measurements.count() > 10 else hs[1].measurements.count()

        url = reverse("api:measurement-list", kwargs={"pk": hs[1].pk})

        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()["data"]), hs_len)


@tag("hs_crud")
class HydroponicSystemRetrieveUpdateDestroyAPIViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(HydroponicSystemRetrieveUpdateDestroyAPIViewTestCase, cls).setUpClass()
        user = UserFactory()
        HydroponicSystemFactory(owner=user)

    def setUp(self):
        self.user = User.objects.first()
        self.url = partial(reverse, "api:rud-hydroponic-system")

    def test_should_delete_a_hydroponic_system(self):
        hs = HydroponicSystem.objects.filter(owner=self.user)
        hs_single_instance = hs.first()
        amt_hs = hs.count()

        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.delete(self.url(kwargs={"pk": hs_single_instance.pk}))

        self.assertEqual(HydroponicSystem.objects.count(), amt_hs - 1)

    def test_should_put_a_hydroponic_system(self):
        hs = HydroponicSystem.objects.filter(owner=self.user)
        hs_single_instance = hs.first()
        payload = {
            "name": "Test Hydroponic System",
            "description": "test description",
            "system_type": HydroponicsType.DRIPPER_FEED,
        }

        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.put(
            self.url(kwargs={"pk": hs_single_instance.pk}), payload, format="json"
        )

        self.assertNotEquals(hs_single_instance.description, payload["description"])
        self.assertNotEquals(hs_single_instance.name, payload["name"])

    def test_should_get_a_hydroponic_system(self):
        hs = HydroponicSystem.objects.filter(owner=self.user)
        hs_single_instance = hs.first()

        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(self.url(kwargs={"pk": hs_single_instance.pk}))

        data = response.json()

        self.assertEqual(hs_single_instance.name, data["name"])
        self.assertEqual(hs_single_instance.description, data["description"])
        self.assertEqual(hs_single_instance.location, data["location"])
        self.assertEqual(hs_single_instance.system_type, data["system_type"])
        self.assertEqual(hs_single_instance.is_active, data["is_active"])

    def test_should_not_get_information_when_user_is_not_owner(self):
        new_user = UserFactory()
        hs = HydroponicSystem.objects.first()
        self.client.login(username=new_user.username, password=PASSWORD)
        response = self.client.get(self.url(kwargs={"pk": hs.pk}))

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
