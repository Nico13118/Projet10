from rest_framework.permissions import BasePermission


class IsUserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
