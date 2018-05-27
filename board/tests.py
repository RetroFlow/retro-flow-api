from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import team


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, team.Profile)

        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instance
        user.save()
        self.assertIsInstance(user.profile, team.Profile)
