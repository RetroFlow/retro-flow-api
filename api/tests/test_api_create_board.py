import json

from django.test import tag
from unittest_data_provider import data_provider

from api.tests import utils
from board.models import Board
from staticfiles import urls
from .test_api_base import BaseTest


class TestCreateBoardApi(BaseTest):

    valid_board_configuration = lambda: (
        ({'name': 'random board name', 'settings': utils.get_default_settings()},),
    )
    invalid_board_configuration = lambda: (
        ({'name': '', 'settings': utils.get_default_settings()},),
    )

    @tag('board_creation')
    @data_provider(valid_board_configuration)
    def test_create_board(self, board_configuration):
        response = self.client.post(urls.core_boards, content_type='application/json',
                                    data=json.dumps(board_configuration), **self.header)
        # assert creation code returned
        self.assertEqual(response.status_code, 201)
        # assert settings are saved
        board = Board.objects.select_related('settings').get(name=board_configuration['name'])
        self.assertIsNotNone(board.settings)
        # assert new team is created
        team = board.team
        self.assertIsNotNone(team)
        # assert board status is new
        self.assertEqual(board.status, Board.Status.NEW)

    @tag('board_creation')
    @data_provider(invalid_board_configuration)
    def test_create_board_negative(self, board_configuration):
        response = self.client.post(urls.core_boards, content_type='application/json',
                                    data=json.dumps(board_configuration), **self.header)
        # assert bad request error
        self.assertEqual(response.status_code, 400)
        # aasert board is not created
        with self.assertRaises(Exception):
            Board.objects.select_related('settings').get(name=board_configuration['name'])
