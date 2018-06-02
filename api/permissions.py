from rest_framework import permissions
from board.models import MembershipInfo


def is_creator(request, obj):
    MembershipInfo.objects.get(profile_id=request.user.profile.id, team_id=obj.board.team.id).role.is_creator()


def is_admin_or_creator(request, obj):
    MembershipInfo.objects.get(profile_id=request.user.profile.id, team_id=obj.board.team.id).role.is_admin_or_creator()


def is_author(request, obj):
    return obj.author.id == request.user.profile.id


def is_read(view):
    return view.action == 'list' or view.action == 'retrieve'


def is_team_member(request, obj):
    return obj.board.team.members.filter(id=request.user.profile.id).count() > 0


class IsCreator(permissions.BasePermission):
    message = 'Action not allowed for non-creator.'

    def has_object_permission(self, request, view, obj):
        return is_creator(request, obj)


class IsCreatorOrAdmin(permissions.BasePermission):
    message = 'Action not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return is_admin_or_creator(request, obj)


class IsAuthorOrAdmin(permissions.BasePermission):
    message = 'Action is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return is_author(request, obj) or is_admin_or_creator(request, obj)


class IsReadOrAdmin(permissions.BasePermission):
    message = 'Modification is not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return is_read(view) or is_admin_or_creator(request, obj)


class IsAuthorOrAdminOrRead(permissions.BasePermission):
    message = 'Modification is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return is_read(view) or is_admin_or_creator(request, obj) or is_author(request, obj)


class IsTeamMember(permissions.BasePermission):
    message = 'Modification is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return is_team_member(request, obj)


class IsAuthor(permissions.BasePermission):
    message = 'Modification is allowed only for admin or author.'

    def has_object_permission(self, request, view, obj):
        return is_author(request, obj)

