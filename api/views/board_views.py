from rest_framework.views import APIView
from ..serializers.board_serializers import BoardSettingsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from board.servises import get_default_board_setting


class BoardSettingsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSettingsSerializer

    def get(self, request):

        settings = get_default_board_setting()

        serializer = self.serializer_class(settings, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


