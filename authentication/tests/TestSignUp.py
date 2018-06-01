from authentication.models import User
from staticfiles import urls
from staticfiles.test_data import User_authentication as TestUser
from .BaseTest import BaseTest


class TestSignUp(BaseTest):

    def test_registration_with_auto_username_creation(self):
        expected_user = User(email=TestUser.email, password=TestUser.password)
        response = self.client.post(urls.users_sign_up, expected_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, expected_user.username)
        actual_user = User.objects.get_by_natural_key(expected_user.username)
        self.assertIsNotNone(actual_user)

    def test_registration(self):
        expected_user = User(email=TestUser.email, password=TestUser.password, username=TestUser.username)
        response = self.client.post(urls.users_sign_up, expected_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, expected_user.username)
        actual_user = User.objects.get_by_natural_key(expected_user.username)
        self.assertIsNotNone(actual_user)
