from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to access the view.
    """

    def has_object_permission(self, request, view, obj):
        if getattr(obj, "owner", obj) == request.user or request.user.is_staff:
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
