from rest_framework.permissions import BasePermission


class IsUserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)
