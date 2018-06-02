User_authentication_models = {
    'username': 'test_user',
    'email': 'test_user@mail.com',
    'password': 'password11'
}
User_authentication_valid_user_1 = {
    'request': {
        'email': 'test_user_1@mail.com',
        'password': 'password11'
    },
    'username': 'test_user_1'
}
User_authentication_valid_user_2 = {
    'request': {
        'username': 'test_user_2',
        'email': 'test_user_2@mail.com',
        'password': 'password11'
    },
    'username': 'test_user_2'
}
User_authentication_valid_user_3 = {
    'request': {
        'username': 'test_user_3',
        'email': 'test_user_3@mail.com',
        'password': 'password11'
    },
    'username': 'test_user_3'
}
User_authentication_invalid_email = {
        'email': 'invalid_email',
        'password': 'password11'
}
User_authentication_too_short_email = {
        'email': '',
        'password': 'password11'
}
User_authentication_too_short_username = {
        'email': 'invalid_username_1@mail.com',
        'username': '',
        'password': 'password11'
}
User_authentication_invalid_username = {
        'email': 'invalid_username_2@mail.com',
        'username': 'valid_username',
        'password': 'password11'
}
User_authentication_too_short_password = {
        'email': 'invalid_password_1@mail.com',
        'username': 'invalid_username',
        'password': 'passw11'
}
User_authentication_password_validation = {
    'request': {
        'email': 'test_user_password_validation@mail.com',
        'password': 'qwerty1234567890`!@#$%^&*()_+=?>\';[]\\{}?|/'
    },
    'username': 'test_user_password_validation'
}
User_authentication_login = {
    'email': 'login_email_1@mail.com',
    'password': 'password11'
}
User_default = {
    'email': 'retroflow@mail.com',
    'password': 'retroflow123'
}
Board_api_create_new_1 = {
    'name': 'test-board-1'
}
