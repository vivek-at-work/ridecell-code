from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where contact_number is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, contact_number, password, **extra_fields):
        """
        Create and save an user with the given contact number and password.
        """
        if not contact_number:
            raise ValueError(_('Contact number must be set'))
        user = self.model(contact_number=contact_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, contact_number, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(contact_number, password, **extra_fields)
