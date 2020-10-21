from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import validate_contact_number

USER = get_user_model()


class SignUpSerializer(serializers.Serializer):
    """
    Sign Up Serializer used for user sign up request validation
    """
    contact_number = serializers.CharField(
        validators=[validate_contact_number,
                    UniqueValidator(
                        queryset=USER.objects.all(),
                        message=_('contact_number is already registered'))],
    )
    password = serializers.CharField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User HyperlinkedModelSerializer Serializer used for user listing
    """
    class Meta:
        model = USER
        fields = ('url', 'contact_number')
