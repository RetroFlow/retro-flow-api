from django.test import TestCase, Client

from api.tests.utils import create_test_user_api, login


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        create_test_user_api()
        token = login(cls.client)
        print(token)
        cls.header = {'HTTP_AUTHORIZATION': token}

    @classmethod
    def tearDownClass(cls):
        pass