from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    message = 'Action not allowed for non-creator.'

    def has_object_permission(self, request, view, obj):
        return request.user.profile.teams.filter(id=obj.board.team.id).role.is_creator()


class IsCreatorOrAdmin(permissions.BasePermission):
    message = 'Action not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return request.user.profile.teams.filter(id=obj.board.team.id).role.is_admin_or_creator()


class IsAuthorOrAdmin(permissions.BasePermission):
    message = 'Action not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.profile.id or \
            request.user.profile.teams.filter(id=obj.board.team.id).role.is_admin_or_creator()


class IsReadOrAdmin(permissions.BasePermission):
    message = 'Action not allowed for non-admin.'

    def has_object_permission(self, request, view, obj):
        return view.action == 'list' or view.action == 'retrieve' or \
            request.user.profile.teams.filter(id=obj.board.team.id).role.is_admin_or_creator()
