from rest_framework.permissions import BasePermission


class IsUserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsContributor(BasePermission):
    message = None

    def has_object_permission(self, request, view, obj):
        list_contributors = obj.contributors.all()
        info_contrib = [c for c in list_contributors if c == request.user]
        if not info_contrib:
            self.message = "You must be a contributor to this project to be able to access the details."
        return bool(info_contrib)

