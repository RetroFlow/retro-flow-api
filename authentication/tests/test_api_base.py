from django.test import TestCase, Client


class BaseTestApi(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        pass
