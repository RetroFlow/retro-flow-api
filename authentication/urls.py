from django.conf.urls import url

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token
)

from .views import RegistrationAPIView, LogoutAPIView

urlpatterns = [
        url(r'^jwt-obtain/', obtain_jwt_token),
        url(r'^jwt-refresh/', refresh_jwt_token),
        url(r'^jwt-verify/', verify_jwt_token),
        url(r'^users/?$', RegistrationAPIView.as_view()),
        url(r'^users/logout/all/$', LogoutAPIView.as_view(), name="users-logout-all"),
]
