from django.test import TestCase, Client


class BaseTest(TestCase):

    def setUpClass(cls):
        cls.client = Client()
