from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User, Project, Contributor


class RegisterUserListSerializer(ModelSerializer):

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

    class Meta:
        model = Project
        fields = [
            'id', 'created_time', 'author', 'project_name', 'project_description', 'type'
        ]


class ProjectDetailSerializer(ModelSerializer):

    contributor_project = serializers.SerializerMethodField()

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

    class Meta:
        model = Contributor
        fields = [
            'id', 'date_joined', 'user', 'project',
        ]
