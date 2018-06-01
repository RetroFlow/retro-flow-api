from django.test import TestCase, Client


class BaseTestApi(TestCase):

    def setUpClass(cls):
        cls.client = Client()
