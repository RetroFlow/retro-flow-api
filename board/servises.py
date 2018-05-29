from .models import Board, BoardSettings


def get_default_board_setting():
    return BoardSettings.get_default_settings()
