from django.test import TestCase, Client

from api.tests.utils import create_test_user_api, login


class BaseTest(TestCase):
    fixtures = ['board/fixtures/board.yaml', ]

    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()

        cls.client = Client()
        create_test_user_api()
        token = login(cls.client)
        print(token)
        cls.header = {'HTTP_AUTHORIZATION': token}

    @classmethod
    def tearDownClass(cls):
        super(BaseTest, cls).tearDownClass()