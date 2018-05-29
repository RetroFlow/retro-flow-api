from rest_framework.views import APIView
from ..serializers.board_serializers import BoardSettingsSerializer, BoardSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from board.servises import get_default_board_setting
from board.models import Board


class BoardSettingsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSettingsSerializer

    def get(self, request):
        settings = get_default_board_setting()
        return Response(settings, status=status.HTTP_200_OK)


class BoardViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.all()

