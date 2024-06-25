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


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'id', 'created_time', 'author', 'project_name', 'project_description', 'type'
        ]


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = [
            'id', 'date_joined', 'user', 'project',
        ]
