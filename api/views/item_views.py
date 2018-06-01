from rest_framework.views import APIView
from ..serializers.board_serializers import BoardSettingsSerializer, BoardSerializer, SprintSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin,\
    RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from board import servises
from board import models as board_models
from ..serializers import item_serializers as it_s
from ..permissions import IsCreator, IsAuthorOrAdmin, IsCreatorOrAdmin, IsReadOrAdmin, IsAuthorOrAdminOrRead, IsTeamMember, IsAuthor


# class ItemViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
#     serializer_class = it_s.ItemSerializer
#     permission_classes = [IsAuthenticated, IsAuthorOrAdminOrRead]
#
#     def get_queryset(self):
#         return board_models.Item.objects.all()


class VoteViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    serializer_class = it_s.VoteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return board_models.Vote.objects.filter(profile_id=self.request.user.profile.id)


class PlainItemViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = it_s.ItemSerializer

    def get_queryset(self):
        return board_models.Item.objects.all()


class CommentsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated, IsAuthor)
    serializer_class = it_s.CommentSerializer

    def get_queryset(self):
        return board_models.Comment.objects.filter(item_id=self.kwargs['item_pk'])
