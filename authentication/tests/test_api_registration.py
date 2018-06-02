from django.test import tag
from unittest_data_provider import data_provider

from authentication.models import User
from board.models import Profile
from staticfiles import urls
from staticfiles.test_data import *
from .test_api_base import BaseTestApi


class TestRegistrationApi(BaseTestApi):
    valid_registration_data = lambda: (
        (User_authentication_valid_user_1['request'], User_authentication_valid_user_1['username']),
        (User_authentication_valid_user_2['request'], User_authentication_valid_user_2['username']),
        (User_authentication_password_validation['request'], User_authentication_password_validation['username']),
    )

    invalid_registration_data = lambda: (
            (User_authentication_invalid_email,),
            (User_authentication_too_short_email,),
            (User_authentication_too_short_password,)
    )

    @tag('registration')
    @data_provider(valid_registration_data)
    def test_registration(self, request, expected_username):
        response = self.client.post(urls.users_sign_up, data=request)
        self.assertEqual(response.status_code, 201,
                         "\nRequest:\n" + str(request) + "\nResponse" + str(response.data))
        self.assertEqual(response.data['username'], expected_username)

        # assert user is created in database
        actual_user = User.objects.get(username=expected_username)
        self.assertIsNotNone(actual_user)

        # assert user profile is created after user registration
        profile = Profile.objects.get(user_id=actual_user.id)
        self.assertEqual(profile.username, expected_username)

    @tag('registration')
    @data_provider(invalid_registration_data)
    def test_registration_is_failed_when_invalid_data_is_sent(self, request):
        response = self.client.post(urls.users_sign_up, data=request)
        # assert bad request code is returned
        self.assertEqual(response.status_code, 400,
                         "\nRequest:\n" + str(request) + "\n" + str(response.data))
        # assert User is not created
        with self.assertRaises(Exception):
            User.objects.get(email=request['email'])
