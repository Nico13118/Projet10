from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User


class RegisterUserSerializer(ModelSerializer):

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


