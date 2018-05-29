from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from .renderers import UserJSONRenderer

import logging
logger = logging.getLogger(__name__)


class RegistrationAPIView(GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user.logout()

        logger.info("Log out of {}".format(user.email))
        return Response(status=status.HTTP_200_OK)
