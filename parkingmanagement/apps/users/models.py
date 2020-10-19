import re

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


def validate_contact_number(value):
    if not re.match(r'[789]\d{9}$', value):
        raise ValidationError(
            _('%(value)s is not a valid contact number'), params={'value': value},
        )


class User(AbstractBaseUser):
    """
    User Model's Replacement for Django applications
    to use contact number for identity rather than username

    """
    username = None
    contact_number = models.CharField(
        _('Contact Number'),
        max_length=10,
        unique=True,
        validators=[validate_contact_number],
    )
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'contact_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """
        Deny All Permissions to Staff User
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Deny All Module Level Permissions to Staff User
        """
        return self.is_superuser

    def __str__(self):
        return self.contact_number
