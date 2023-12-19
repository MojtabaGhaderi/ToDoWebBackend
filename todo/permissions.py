from rest_framework.permissions import BasePermission

from todo.models import GroupModel


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsGroupHead(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsGroupAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.admin == request.user


class IsInGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        user = request.user
        return GroupModel.objects.filter(id=group_id, members=user).exist()
