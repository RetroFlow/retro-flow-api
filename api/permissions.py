from rest_framework import permissions
from board.models import MembershipInfo


class IsCreator(permissions.BasePermission):
    message = 'Action not allowed for non-creator.'

    def has_object_permission(self, request, view, obj):
        return request.user.profile.teams.filter(id=obj.board.team.id).role.is_creator()


class IsCreatorOrAdmin(permissions.BasePermission):
    message = 'Action not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return request.user.profile.teams.filter(id=obj.board.team.id).role.is_admin_or_creator()


class IsAuthorOrAdmin(permissions.BasePermission):
    message = 'Action is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.profile.id or \
            request.user.profile.teams.filter(id=obj.board.team.id).role.is_admin_or_creator()


class IsReadOrAdmin(permissions.BasePermission):
    message = 'Modification is not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return view.action == 'list' or view.action == 'retrieve' or \
            MembershipInfo.objects.get(profile_id=request.user.profile.id, team_id=obj.board.team.id).role.is_admin_or_creator()


class IsAuthorOrAdminOrRead(permissions.BasePermission):
    message = 'Modification is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.profile.id or \
               view.action == 'list' or view.action == 'retrieve' or \
               request.user.profile.teams.filter(id=obj.board.team.id).role.is_admin_or_creator()


class IsTeamMember(permissions.BasePermission):
    message = 'Modification is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return obj.board.team.members.contains(request.user.profile)

class IsAuthor(permissions.BasePermission):
    message = 'Modification is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.profile.id

