

from authentication.models import User
from staticfiles import urls
from staticfiles.test_data import User_default as TestUser


def login(client):
    response = client.post(urls.users_login, data=TestUser)
    return 'Bearer ' + response.data['token']


def create_test_user_api():
    return create_user(TestUser['email'], TestUser['password'])


def create_user(email, password, username=""):
    if username is not "":
        return User.objects.create_user(email, password, username)
    else:
        return User.objects.create_user(email, password)
