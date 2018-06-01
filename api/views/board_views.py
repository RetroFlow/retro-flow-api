from rest_framework.views import APIView
from ..serializers.board_serializers import BoardSettingsSerializer, BoardSerializer, SprintSerializer, DeepBoardSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin,\
    RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from django.shortcuts import get_object_or_404
from board import servises
from board import models as board_models
from ..serializers import team_serializers as ts
from ..serializers import assignee_serializers as as_ser
from rest_framework.decorators import action
from ..permissions import IsCreator, IsAuthorOrAdmin, IsCreatorOrAdmin, IsReadOrAdmin


class BoardSettingsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSettingsSerializer

    def get(self, request):
        settings = servises.get_default_board_setting()
        return Response(settings, status=status.HTTP_200_OK)


class BoardViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = BoardSerializer

    def get_queryset(self):
        return servises.get_boards(user=self.request.user)

    def perform_create(self, serializer):
        team = servises.create_new_team(self.request.user)
        serializer.save(team_id=team.id)

    @action(permission_classes=[IsCreator], detail=True)
    def destroy(self, request, *args, **kwargs):
        return DestroyModelMixin.destroy(self, request, *args, **kwargs)

    @action(permission_classes=[IsCreator], detail=True, url_path='start_new_sprint', methods=['GET'])
    def start_new_sprint(self, request, *args, **kwargs):
        board = self.get_object()
        board.start_new_sprint()
        sprint = SprintSerializer(board.current_sprint)
        return Response(status=status.HTTP_201_CREATED, data=sprint.data)


class DeepBoardViewSet(GenericViewSet, RetrieveModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = DeepBoardSerializer

    def get_queryset(self):
        return servises.get_boards(user=self.request.user)


class UserProfileViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    permission_classes = (IsAuthenticated, IsReadOrAdmin)
    serializer_class = ts.UserProfileSerializer

    def get_queryset(self):
        return board_models.Profile.objects.all()

    def get_object(self):
        return board_models.Profile.objects.get(id=self.request.user.profile.id)


class TeamViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = ts.TeamSerializer

    def get_queryset(self):
        return servises.get_teams(user=self.request.user)


class TeamMembersViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated, IsReadOrAdmin)
    serializer_class = ts.MembershipSerializer

    def get_queryset(self):
        return board_models.MembershipInfo.objects.filter(team_id=self.kwargs['team_pk'])


class GroupsViewSet(GenericViewSet, ListModelMixin, CreateModelMixin,
                    DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin):
    permission_classes = (IsAuthenticated, IsReadOrAdmin)
    serializer_class = ts.GroupSerializer

    def get_queryset(self):
        return board_models.Group.objects.filter(team_id=self.kwargs['team_pk'])

    @action(methods=['POST'], detail=True, url_path='add_members')
    def add(self, request, *args, **kwargs):

        """
            Add users to the group. Accessible only for Admin or Owner.

            Expected the request body in format {"members": [id, id, id]}

        """

        s = as_ser.GroupMembersSerializer(data=self.request.data)
        s.is_valid(raise_exception=True)
        members = s.data['members']
        group = self.get_object()
        for id in members:
            group.members.add(get_object_or_404(board_models.Profile, pk=id))
        group.save()
        return Response(data=self.serializer_class(group).data,  status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=True, url_path='remove_members')
    def remove(self, request, *args, **kwargs):

        """
            Remove users from the group. Accessible only for Admin or Owner.

            Expected the request body in format {"members": [id, id, id]}

        """

        s = as_ser.GroupMembersSerializer(data=self.request.data)

        s.is_valid(raise_exception=True)

        members = s.data['members']
        group = self.get_object()
        for id in members:
            group.members.remove(get_object_or_404(board_models.Profile, pk=id))
        group.save()
        return Response(data=self.serializer_class(group).data, status=status.HTTP_202_ACCEPTED)
