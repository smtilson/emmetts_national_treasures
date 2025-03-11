from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to access the view.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsFriend(permissions.BasePermission):
    """
    Custom permission to only allow friends to access the view.
    """

    def has_object_permission(self, request, view, obj):
        # I expect this will fail because obj.owner is an id and not a user obj.
        owner = obj.owner
        if request.user in owner.friends.all():
            return True
        return False
