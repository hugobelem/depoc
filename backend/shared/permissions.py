from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if hasattr(user, 'owner'):
            return request.user
