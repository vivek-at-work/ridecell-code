from django.contrib.auth import backends, get_user_model

USER = get_user_model()

class ConatctNumberBasedAuthenticationsBackend(backends.ModelBackend):
    """
    Authenticate users based on contact number instead of username.
    """
    def authenticate(self, request, **kwargs):
        contact_number = kwargs.get('contact_number', None)
        password = kwargs['password']
        if not contact_number:
            # django admin login still sends username
            contact_number = kwargs.get('username', None)
        try:
            user = USER.objects.get(contact_number=contact_number)
            if user.check_password(password) is True:
                return user
            return None
        except USER.DoesNotExist:
            pass
