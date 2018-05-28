from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import User


class TestUserModel(TestCase):

    def test_auto_username_creation(self):

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        user.save()

        self.assertEqual(user.username, "test-user")

    def test_manual_username_creation(self):

        user = User.objects.create(
            email="test-user@mail.com", password="password11", username="test-username")

        self.assertEqual(user.username, "test-username")
