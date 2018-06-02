from django.test import tag
from unittest_data_provider import data_provider

from board import servises
from board.models import Board
from staticfiles import urls
from .test_api_base import BaseTest


class TestCreateBoardApi(BaseTest):

    valid_board_configuration = lambda: (
        ({'name': 'random board name', 'settings': servises.get_default_board_setting()},),
    )
    invalid_board_configuration = lambda: (
        ({'name': '', 'settings': servises.get_default_board_setting()},),
    )

    @tag('board_creation')
    @data_provider(valid_board_configuration)
    def test_create_board(self, board_configuration):
        response = self.client.post(urls.core_boards, content_type='application/json',
                                    data=board_configuration, **self.header)
        # assert creation code returned
        self.assertEqual(response.status_code, 201)
        board = Board.objects.get(name=board_configuration['name'])
        self.assertEqual(board.settings, board_configuration['settings'])

    @tag('board_creation')
    @data_provider(invalid_board_configuration)
    def test_create_board_negative(self, board_configuration):
        response = self.client.post(urls.core_boards, content_type='application/json',
                                    data=board_configuration, **self.header)
        # assert bad request error
        self.assertEqual(response.status_code, 400)
