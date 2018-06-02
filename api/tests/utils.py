from authentication.models import User
from board import servises
from staticfiles import urls
from staticfiles.test_data import User_default as TestUser


def login(client):
    User.objects.get(email=TestUser['email'])
    response = client.post(urls.users_login, data=TestUser)
    return 'Bearer ' + response.data['token']


def create_test_user_api():
    try:
        User.objects.create_user(TestUser['email'], TestUser['password'])
    except Exception:
        pass


def get_default_settings():
    default_settings = servises.get_default_board_setting()
    default_settings['sprint_start_date'] = default_settings['sprint_start_date'].isoformat()
    return default_settings
