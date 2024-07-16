from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from softdesk.models import User, Project, Contributor
from softdesk.permissions import IsUserAuthenticated, IsSuperUser
from softdesk.serializers import RegisterUserListSerializer, ProjectListSerializer, ContributorSerializer, \
    ProjectDetailSerializer, ContributorDetailSerializer

# ModelViewSet : create()`, `retrieve()`, `update()`,
# `partial_update()`, `destroy()`, `list()`


class MultipleSerializerMixin(ModelViewSet):
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class RegisterUserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserListSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]

        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            self.permission_classes = [IsUserAuthenticated]
        else:
            self.permission_classes = [IsSuperUser]

        return super().get_permissions()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            self.permission_classes = [IsUserAuthenticated]
        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Avant l'enregistrement d'un contributeur, deux contrôles sont effectués :
        1) Vérifie que l'utilisateur connecté soit bien l'auteur du projet.
        2) Vérifie que l'utilisateur selectionné dans le formulaire ne soit pas déjà contributeur du projet.

        Si l'un de ces contrôles échoue, une ValildationError est levée.
        """
        get_user_id_auth = self.request.user.id  # Récuperation de l'id de l'utilisateur connecté
        get_project_id_form = self.request.data.get('project')  # Récuperation de (project_id) depuis le formulaire
        get_project_name = Project.objects.get(id=get_project_id_form)  # Récupère le nom du projet au format str
        exist_project_name_author = Project.objects.filter(author=get_user_id_auth,
                                                           project_name=get_project_name).exists()
        """ Si l'utiliateur connecté est bien l'auteur du projet selectionné dans le formulaire."""
        if exist_project_name_author:
            get_user_id_form = self.request.data.get('user')  # Récupération du (user_id) depuis le formulaire
            user_name = User.objects.get(id=get_user_id_form)  # Récupérer le nom du (user) avec son id.
            exist_contributor_in_project = self.queryset.filter(user=user_name,
                                                                project=get_project_name).exists()
            """ Si l'utilisateur selectionné dans le formulaire est déjà contributeur de ce projet."""
            if exist_contributor_in_project:
                raise ValidationError("The chosen user is already a contributor to this project.")
            else:
                serializer.save(user=user_name, project=get_project_name)
        else:
            raise ValidationError("You are not allowed to add a contributor for this project.")
