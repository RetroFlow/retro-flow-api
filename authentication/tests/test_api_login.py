from django.test import tag
from unittest_data_provider import data_provider

from authentication.models import User
from authentication.tests import BaseTestApi
from staticfiles import urls
from staticfiles.test_data import user_authentication_login as user


class TestLoginApi(BaseTestApi):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(email=user['email'], password=user['password'])


    invalid_login_data = lambda: (
        (
            {'email': 'login_email_1', 'password': user['password']},
        ),
        (
            {'email': user['email'], 'password': '*'},
        )
    )

    @tag('login')
    def test_login(self):
        response = self.client.post(urls.users_login, data=user)
        self.assertEqual(response.status_code, 200,
                         "\nRequest:\n" + str(user) + "\nResponse" + str(response))
        self.assertIsNotNone(response.data['token'])

    @tag('login')
    @data_provider(invalid_login_data)
    def test_login_negative(self, credentials):
        response = self.client.post(urls.users_login, data=credentials)
        self.assertEqual(response.status_code, 400,
                         "\nRequest:\n" + str(credentials) + "\nResponse" + str(response))
