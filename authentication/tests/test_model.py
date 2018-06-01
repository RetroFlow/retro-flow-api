from django.test import TestCase

from authentication.models import User
from staticfiles.test_data import User_authentication_models as TestUser


class TestUserModel(TestCase):
    def test_auto_username_creation(self):

        user = User.objects.create(
            email=TestUser['email'], password=TestUser['password'])
        user.save()

        self.assertEqual(user.username, TestUser['username'])

    def test_manual_username_creation(self):

        user = User.objects.create(
            email=TestUser['email'], password=TestUser['password'], username=TestUser['username'])

        self.assertEqual(user.username, TestUser['username'])

