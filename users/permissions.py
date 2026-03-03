from rest_framework import permissions


class IsExpert(permissions.BasePermission):
    """Allow access only to users marked as experts."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_expert)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners to edit/delete an object."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute 'expert' or 'user'
        owner = getattr(obj, 'expert', None) or getattr(obj, 'user', None) or getattr(obj, 'client', None)
        if owner is None:
            return False
        # If owner is a profile, compare the user
        if hasattr(owner, 'user'):
            return owner.user == request.user
        return owner == request.user
