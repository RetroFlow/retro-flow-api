from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from board import models as board_models
from ..import serializers
from .. import permissions


class VoteViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.VoteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return board_models.Vote.objects.filter(profile_id=self.request.user.profile.id)


class PlainItemViewSet(GenericViewSet,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = (IsAuthenticated, permissions.IsAuthorOrAdminOrRead)
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        return board_models.Item.objects.all()


class CommentsViewSet(GenericViewSet,
                      mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin, mixins.DestroyModelMixin):

    permission_classes = (IsAuthenticated, permissions.IsAuthorOrAdminOrRead)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return board_models.Comment.objects.filter(item_id=self.kwargs['item_pk'])
