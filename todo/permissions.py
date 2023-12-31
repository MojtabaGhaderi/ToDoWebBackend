from rest_framework.permissions import BasePermission

from todo.models import GroupModel


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsSelfFriendResponse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user


class GroupJoinInvitationResponsePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.invited == request.user


class FriendListEditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user1 == request.user or obj.user2 == request.user


class IsGroupHead(BasePermission):
    def has_object_permission(self, request, view, obj):
        # group = obj.group
        creator = obj.creator
        return creator == request.user


class IsGroupAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        group = obj.group
        admins = group.admin
        if admins is None:
            return False
        else:
            return request.user in admins


class IsGroupHeadOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            IsGroupHead().has_object_permission(request, view, obj)
            or
            IsGroupAdmin().has_object_permission(request, view, obj)
        )


class IsInGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        user = request.user
        return GroupModel.objects.filter(id=group_id, members=user).exist()


class IsTaskOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user