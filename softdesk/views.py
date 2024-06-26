from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from softdesk.models import User, Project, Contributor
from softdesk.permissions import IsUserAuthenticated, IsSuperUser
from softdesk.serializers import RegisterUserListSerializer, ProjectListSerializer, ContributorSerializer


# ModelViewSet : create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()`, `list()`

class RegisterUserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserListSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]

        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()


class ProjectViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsUserAuthenticated]
        else:
            self.permission_classes = [IsSuperUser]

        return super().get_permissions()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewset(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsUserAuthenticated]
        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()

