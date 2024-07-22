from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from softdesk.models import User, Project, Contributor, Issue
from softdesk.permissions import IsUserAuthenticated, IsSuperUser, IsContributor
from softdesk.serializers import RegisterUserListSerializer, ProjectListSerializer, ContributorSerializer, \
    ProjectDetailSerializer, ContributorDetailSerializer, IssueSerializer


# ModelViewSet : create()`, `retrieve()`, `update()`,
# `partial_update()`, `destroy()`, `list()`


class GetObjects:

    @classmethod
    def get_objects_all_models(cls, model_name, info_id=None):
        """
        Fonction à double utilité :
        1) Si info_id est None : On retourne tous les objets selon le modèle spécifié (model_name).
        2) Sinon : On retourne l'objet selon le modèle (model_name) et l'id spécifié (info_id).
        """
        if info_id is None:
            obj_model = model_name.objects.all()
        else:
            obj_model = model_name.objects.get(id=info_id)
        return obj_model


class MultipleSerializerMixin(ModelViewSet):
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class RegisterUserViewset(ModelViewSet):
    queryset = GetObjects.get_objects_all_models(User)
    serializer_class = RegisterUserListSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]

        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    queryset = GetObjects.get_objects_all_models(Project)
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            """ Seuls les utilisateurs authentifiés peuvent créer et voir la liste des projets """
            self.permission_classes = [IsUserAuthenticated]
        elif self.action == 'retrieve':
            """ Seuls les contributeurs peuvent accéder aux détails d'un projet"""
            self.permission_classes = [IsContributor]
        else:
            self.permission_classes = [IsSuperUser]

        return super().get_permissions()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):
    queryset = GetObjects.get_objects_all_models(Contributor)
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
        obj_user_auth = self.request.user
        obj_project = GetObjects.get_objects_all_models(Project, self.request.data.get('project'))
        """ 
        Recherche que l'utilisateur connecté est bien l'auteur du projet selectionné dans le formulaire et 
        retourne True ou False.
        """
        exist_project_name_author = Project.objects.filter(author=obj_user_auth,
                                                           project_name=obj_project).exists()
        if exist_project_name_author:
            obj_user_form = GetObjects.get_objects_all_models(User, self.request.data.get('user'))

            """ Recherche que l'utilisateur selectionné dans le formulaire est déjà contributeur de ce projet."""
            exist_contributor_in_project = self.queryset.filter(user=obj_user_form,
                                                                project=obj_project).exists()
            if exist_contributor_in_project:
                raise ValidationError("The chosen user is already a contributor to this project.")
            else:
                serializer.save(user=obj_user_form, project=obj_project)
        else:
            raise ValidationError("You are not allowed to add a contributor for this project.")


class IssueViewset(ModelViewSet):
    queryset = GetObjects.get_objects_all_models(Issue)
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            self.permission_classes = [IsUserAuthenticated]
        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Avant l'enregistrement de l'issue, deux contrôles sont effectués : :
        1) Vérifier que l'utilisateur connecté soit bien contributeur du projet selectionné dans le formulaire.
        2) Vérifier que l'utilisateur sélectionné dans le formulaire est contributeur du projet.

        Si l'un de ces contrôles échoue, une ValildationError est levée.
        """
        """ Récupérer l'objet de l'utilisateur connecté """
        obj_user_auth = self.request.user
        """ Récupérer l'objet du projet en provenance du formulaire"""
        obj_project = GetObjects.get_objects_all_models(Project, self.request.data.get('project'))

        """ Recherche que l'utilisateur connecté est bien contributeur du projet et retourne True ou False """
        exist_contributor_in_project = Contributor.objects.filter(user=obj_user_auth,
                                                                  project=obj_project).exists()
        if exist_contributor_in_project:
            """ Récupérer l'objet utilisateur assigné à l'Issue"""
            obj_user_form = GetObjects.get_objects_all_models(User, self.request.data.get('assigned_contributor'))

            """ Recherche que l'utilisateur selectionné dans le formulaire est bien contributeur du projet"""
            exist_contributor_in_project2 = Contributor.objects.filter(user=obj_user_form,
                                                                       project=obj_project).exists()
            if exist_contributor_in_project2:
                serializer.save(author=obj_user_auth,
                                assigned_contributor=obj_user_form,
                                project=obj_project)
            else:
                raise ValidationError("The chosen user is not a contributor to this project.")

        else:
            raise ValidationError("You cannot create an Issue because you are not a contributor to this project.")
