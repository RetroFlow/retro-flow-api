from django.test import tag

from api.tests.test_api_base import BaseTest
from staticfiles import urls


class TestGetDefaultBoardSettings(BaseTest):
    @tag('board')
    def test_get_default_board_settings(self):
        default_settings = self.client.get(urls.core_default_settings, **self.header)
        print(default_settings.json())