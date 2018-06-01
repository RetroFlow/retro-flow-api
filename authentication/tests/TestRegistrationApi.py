from authentication.models import User
from staticfiles import urls
from staticfiles.test_data import User_authentication_1 as FirstTestUser
from staticfiles.test_data import User_authentication_2 as SecondTestUser
from .BaseTestApi import BaseTestApi


class TestRegistrationApi(BaseTestApi):

    def test_registration_with_auto_username_creation(self):
        expected_user = User(email=FirstTestUser.email, password=FirstTestUser.password)
        response = self.client.post(urls.users_sign_up, expected_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body.username, expected_user.username)
        actual_user = User.objects.get_by_natural_key(expected_user.username)
        self.assertIsNotNone(actual_user)

    def test_registration(self):
        expected_user = User(email=FirstTestUser.email, password=FirstTestUser.password, username=FirstTestUser.username)
        response = self.client.post(urls.users_sign_up, expected_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body.username, expected_user.username)
        actual_user = User.objects.get_by_natural_key(expected_user.username)
        self.assertIsNotNone(actual_user)

    def test_failed_registration_with_invalid_email(self):
        expected_user = User(email='invalid_email', password=FirstTestUser.password)
        response = self.client.post(urls.users_sign_up, expected_user)
        self.assertEqual(response.status_code, 404)

    def test_registration_with_special_symbols_in_password(self):
        expected_user = User(email=SecondTestUser.email, password=SecondTestUser.password)
        response = self.client.post(urls.users_sign_up, expected_user)
        self.assertEqual(response.status_code, 200)
        actual_user = User.objects.get_by_natural_key(expected_user.username)
        self.assertIsNotNone(actual_user)
