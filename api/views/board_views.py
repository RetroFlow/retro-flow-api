from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status, views, decorators
from django.shortcuts import get_object_or_404
from board import servises
from board import models as board_models
from .. import serializers
from .. import permissions


class BoardSettingsApiView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BoardSettingsSerializer

    def get(self, request):
        settings = servises.get_default_board_setting()
        return Response(settings, status=status.HTTP_200_OK)


class BoardViewSet(GenericViewSet,
                   mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return servises.get_boards(user=self.request.user)

    def perform_create(self, serializer):
        team = servises.create_new_team(self.request.user)
        serializer.save(team_id=team.id)

    @decorators.action(permission_classes=[permissions.IsCreator], detail=True)
    def destroy(self, request, *args, **kwargs):
        return mixins.DestroyModelMixin.destroy(self, request, *args, **kwargs)

    @decorators.action(permission_classes=[permissions.IsCreator], detail=True, url_path='start_new_sprint', methods=['GET'])
    def start_new_sprint(self, request, *args, **kwargs):
        board = self.get_object()
        board.start_new_sprint()
        sprint = serializers.SprintSerializer(board.current_sprint)
        return Response(status=status.HTTP_201_CREATED, data=sprint.data)


class DeepBoardViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.DeepBoardSerializer

    def get_queryset(self):
        return servises.get_boards(user=self.request.user)


class UserProfileViewSet(GenericViewSet,
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.ListModelMixin):
    permission_classes = (IsAuthenticated, permissions.IsReadOrAdmin)
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        return board_models.Profile.objects.all()

    def get_object(self):
        return board_models.Profile.objects.get(id=self.request.user.profile.id)


class TeamViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.TeamSerializer

    def get_queryset(self):
        return servises.get_teams(user=self.request.user)


class TeamMembersViewSet(GenericViewSet,
                         mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.DestroyModelMixin):

    permission_classes = (IsAuthenticated, permissions.IsReadOrAdmin)
    serializer_class = serializers.MembershipSerializer

    def get_queryset(self):
        return board_models.MembershipInfo.objects.filter(team_id=self.kwargs['team_pk'])


class GroupsViewSet(GenericViewSet,
                    mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated, permissions.IsReadOrAdmin)
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        return board_models.Group.objects.filter(team_id=self.kwargs['team_pk'])

    @decorators.action(methods=['POST'], detail=True, url_path='add_members')
    def add(self, request, *args, **kwargs):

        """
            Add users to the group. Accessible only for Admin or Owner.

            Expected the request body in format {"members": [id, id, id]}

        """

        s = serializers.GroupMembersSerializer(data=self.request.data)
        s.is_valid(raise_exception=True)
        members = s.data['members']
        group = self.get_object()
        for id in members:
            group.members.add(get_object_or_404(board_models.Profile, pk=id))
        group.save()
        return Response(data=self.serializer_class(group).data,  status=status.HTTP_202_ACCEPTED)

    @decorators.action(methods=['POST'], detail=True, url_path='remove_members')
    def remove(self, request, *args, **kwargs):

        """
            Remove users from the group. Accessible only for Admin or Owner.

            Expected the request body in format {"members": [id, id, id]}

        """

        s = serializers.GroupMembersSerializer(data=self.request.data)

        s.is_valid(raise_exception=True)

        members = s.data['members']
        group = self.get_object()
        for id in members:
            group.members.remove(get_object_or_404(board_models.Profile, pk=id))
        group.save()
        return Response(data=self.serializer_class(group).data, status=status.HTTP_202_ACCEPTED)
