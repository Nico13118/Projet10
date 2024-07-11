from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User, Project, Contributor


class RegisterUserListSerializer(ModelSerializer):
    """
    Permet l'enregistrement d'un utilisateur.
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'age', 'password', 'can_be_contacted',
            'can_data_be_shared'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_age(self, value):
        if value < 16:
            raise ValidationError('You are not old enough to register.')
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjectListSerializer(ModelSerializer):
    """
    Permet d'avoir la liste des projets
    """

    class Meta:
        model = Project
        fields = [
            'id', 'created_time', 'author', 'project_name', 'project_description', 'type'
        ]
        read_only_fields = ['author']


class ProjectDetailSerializer(ModelSerializer):
    """
    Permet d'avoir le détail d'un projet et la liste des contributeurs
    """
    contributor_project = serializers.SerializerMethodField()  # contributor_project = model Contributor

    class Meta:
        model = Project
        fields = [
            'id', 'created_time', 'author', 'project_name', 'project_description', 'type', 'contributor_project'
        ]

    def get_contributor_project(self, instance):
        queryset = instance.contributor_project.all()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(ModelSerializer):
    """
    Permet d'avoir la liste des contributeurs liés à chaques projets.
    """

    class Meta:
        model = Contributor
        fields = [
            'id', 'user', 'project', 'date_joined'
        ]


class ContributorDetailSerializer(ModelSerializer):

    """
    Permet d'avoir le détail d'un contributeur et la liste des projets qu'il suit.
    """
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = [
            'user', 'projects'
        ]

    def get_projects(self, obj):
        projects = Contributor.objects.filter(user=obj.user)

        return ContributorSerializer(projects, many=True).data


