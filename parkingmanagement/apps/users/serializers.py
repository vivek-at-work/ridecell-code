from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import validate_contact_number

USER = get_user_model()

class SignUpSerializer(serializers.Serializer):
    """
    Sign Up Serializer used for user sign up request validation
    """
    contact_number = serializers.CharField(
        validators=[validate_contact_number],
    )
    password = serializers.CharField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User HyperlinkedModelSerializer Serializer used for user listing
    """
    class Meta:
        model = USER
        fields = ('url', 'contact_number')
