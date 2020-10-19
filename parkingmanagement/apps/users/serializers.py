from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import validate_contact_number

USER = get_user_model()


def validate_contact_number_is_unique(value):
    if USER.objects.filter(contact_number=value).exists():
        raise ValidationError(
            _('%(value)s is already registered'), params={'value': value},
        )
class SignUpSerializer(serializers.Serializer):
    """
    Sign Up Serializer used for user sign up request validation
    """
    contact_number = serializers.CharField(
        validators=[validate_contact_number,
                    validate_contact_number_is_unique],
    )
    password = serializers.CharField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User HyperlinkedModelSerializer Serializer used for user listing
    """
    class Meta:
        model = USER
        fields = ('url', 'contact_number')
