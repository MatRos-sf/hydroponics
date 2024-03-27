import uuid
from http import HTTPStatus

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, tag
from faker import Faker
from parameterized import parameterized

from hydroponics_manager.factories import PASSWORD, HydroponicSystemFactory, UserFactory
from hydroponics_manager.models import HydroponicsType, HydroponicSystem


@tag("cl")
class CustomLogoutViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CustomLogoutViewTest, cls).setUpClass()
        UserFactory(username="testuser")

    def setUp(self):
        self.user = User.objects.first()
        self.url = reverse("hydroponic_system:logout")

    def test_should_logout_user_when_user_is_authenticated(self):
        self.client.login(username="testuser", password=PASSWORD)
        self.assertTrue(get_user(self.client).is_authenticated)

        self.client.get(self.url)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_do_nothing_when_user_is_not_authenticated(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        self.client.get(self.url)
        self.assertFalse(get_user(self.client).is_authenticated)


@tag("su")
class SignUpViewTest(TestCase):
    def setUp(self):
        fake = Faker()
        self.url = reverse("hydroponic_system:signup")
        self.payload = {
            "username": "testuser",
            "password1": PASSWORD,
            "password2": PASSWORD,
            "email": fake.email(),
        }

    def test_should_create_user_when_payload_is_valid(self):
        self.assertFalse(User.objects.count())

        self.client.post(self.url, data=self.payload)

        self.assertEqual(User.objects.count(), 1)

    def test_should_redirect_status_code_when_payload_is_valid(self):
        response = self.client.post(self.url, data=self.payload)
        self.assertRedirects(response, reverse("hydroponic_system:login"))

    def test_should_not_create_user_when_user_does_not_have_unique_email(self):
        email = "test@localhost.com"
        UserFactory(email=email)
        payload = self.payload
        payload["email"] = email

        self.client.post(self.url, data=payload)

        self.assertFalse(User.objects.count() == 2)

    def test_should_return_message_when_user_was_created(self):
        expected_message = "User was created successfully"
        self.assertFalse(User.objects.count())

        response = self.client.post(self.url, data=self.payload, follow=True)

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)


@tag("hsc")
class HydroponicSystemCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(HydroponicSystemCreateViewTestCase, cls).setUpClass()
        UserFactory()

    def setUp(self):
        self.user = User.objects.first()
        self.url = reverse("hydroponic_system:create")
        self.payload = {
            "name": "Test Hydroponic System",
            "system_type": HydroponicsType.POT,
        }

    def test_should_create_new_hydroponic_system_when_payload_is_valid(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.post(self.url, data=self.payload)

        self.assertEqual(HydroponicSystem.objects.count(), 1)

    def test_should_assign_owner_when_payload_is_valid(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.post(self.url, data=self.payload)

        hs = HydroponicSystem.objects.first()
        self.assertEqual(hs.owner, self.user)

    def test_should_not_created_when_user_is_not_authenticated(self):
        self.client.post(self.url, data=self.payload)

        self.assertFalse(HydroponicSystem.objects.count())

    @parameterized.expand([({"system_type": HydroponicsType.POT},), ({},)])
    def test_should_not_create_when_payload_does_not_have_required_fields(
        self, payload
    ):
        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.post(self.url, data=payload)

        self.assertFalse(HydroponicSystem.objects.count())

    def test_should_redirect_when_created_model(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(self.url, data=self.payload)

        instance = HydroponicSystem.objects.first()
        self.assertRedirects(response, instance.get_absolute_url())

    def test_when_user_write_wrong_system_type_then_instance_does_not_create(self):
        payload = self.payload
        payload["system_type"] = "test"
        self.client.post(self.url, data=payload)

        instance = HydroponicSystem.objects.first()

        self.assertIsNone(instance)


class CustomDataBaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CustomDataBaseTestCase, cls).setUpClass()
        user = UserFactory()
        HydroponicSystemFactory(owner=user)


@tag("hsu")
class HydroponicSystemUpdateViewTestCase(CustomDataBaseTestCase):
    def setUp(self):
        self.url_name = "hydroponic_system:update"
        self.user = User.objects.first()
        self.hs = HydroponicSystem.objects.first()

    def test_should_update_when_user_is_owner(self):
        new_data = {
            "name": "new_test",
            "description": "new_description",
            "system_type": HydroponicsType.NFT,
        }

        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.post(
            reverse(self.url_name, kwargs={"pk": self.hs.pk}), data=new_data
        )

        instance = HydroponicSystem.objects.first()

        self.assertEqual(instance.name, new_data["name"])
        self.assertEqual(instance.description, new_data["description"])

    def test_should_return_forbidden_when_user_is_not_owner(self):
        new_user = UserFactory()
        self.client.login(username=new_user.username, password=PASSWORD)
        response = self.client.post(
            reverse(self.url_name, kwargs={"pk": self.hs.pk}), data={}
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


@tag("hsd")
class HydroponicSystemDeleteViewTestCase(CustomDataBaseTestCase):
    def setUp(self):
        self.user = User.objects.first()
        self.url_name = "hydroponic_system:delete"

    def test_should_delete_and_redirect_when_user_is_owner(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        pk = self.user.systems.first().pk

        response = self.client.post(reverse(self.url_name, kwargs={"pk": pk}))

        self.assertEqual(HydroponicSystem.objects.count(), 0)
        self.assertRedirects(response, reverse("hydroponic_system:list"))

    def test_should_not_delete_when_user_is_not_owner(self):
        new_user = UserFactory()
        self.client.login(username=new_user.username, password=PASSWORD)

        response = self.client.post(reverse(self.url_name, kwargs={"pk": 1}))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


@tag("hsl")
class HydroponicSystemListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(HydroponicSystemListViewTestCase, cls).setUpClass()
        user_one, user_two = UserFactory.create_batch(2)

        for _ in range(5):
            HydroponicSystemFactory(owner=user_one, name=f"name_{_}")

        for _ in range(10):
            HydroponicSystemFactory(owner=user_two)
        # HydroponicSystemFactory.create_batch(5, owner=user_one)
        # HydroponicSystemFactory.create_batch(10, owner=user_two)

    def setUp(self):
        self.user_one = User.objects.first()
        self.user_two = User.objects.last()
        self.url = reverse("hydroponic_system:list")

    def test_should_show_only_hydroponic_system_who_belong_to_users(self):
        # first user
        self.client.login(username=self.user_one.username, password=PASSWORD)
        response = self.client.get(self.url)
        object_list = response.context_data["object_list"]

        self.assertEqual(len(object_list), 5)

        # second user
        self.client.login(username=self.user_two.username, password=PASSWORD)
        response = self.client.get(self.url)
        object_list = response.context_data["object_list"]

        self.assertEqual(len(object_list), 10)
