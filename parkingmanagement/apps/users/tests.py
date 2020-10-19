from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .backends import ConatctNumberBasedAuthenticationsBackend

USER = get_user_model()

class UsersTestCase(TestCase):


    def test_normal_user_creation(self):
        """Test Normal User Creation"""
        u = USER.objects.create_user('9657946755', 'Qwerty@1234')
        assert u.contact_number == '9657946755'
        assert u.is_staff == True
        assert u.is_superuser == False
        assert u.has_perm('', None) == False
        assert u.has_module_perms('') == False


    def test_super_user_creation(self):
        """Test Super User Creation"""
        u = USER.objects.create_superuser('9657946756', 'Qwerty@1234')
        assert u.contact_number == '9657946756'
        assert u.is_staff == True
        assert u.is_superuser == True
        assert u.has_perm('', None) == True
        assert u.has_module_perms('') == True
        assert str(u) == u.contact_number


class ConatctNumberBasedAuthenticationsBackendTestCase(TestCase):
    def setUp(self):
        USER.objects.create_user('9657946755', 'Qwerty@1234')

    def test_user_login(self):
        """Test Existing User can login"""
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username='9657946755', password='Qwerty@1234',
        )
        assert str(t) == '9657946755'

    def test_non_user_login(self):
        """Test Non Existing User User Login"""
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username='9657906755', password='Qwerty@1234',
        )
        assert t is None


class UsersAPITests(APITestCase):
    def test_user_signup(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user-signup')
        payload = {
            'contact_number': '9657946755',
            'password': 'Qwerty@1234',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username='9657946755', password='Qwerty@1234',
        )
        assert str(t) == '9657946755'


    def test_user_list(self):
        """
        Ensure we can create a new user object and get the same in list.
        """
        url = reverse('user-signup')
        payload = {
            'contact_number': '9657946755',
            'password': 'Qwerty@1234',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username='9657946755', password='Qwerty@1234',
        )
        self.client.login(username='9657946755', password='Qwerty@1234')
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        assert len(response.data) == 1
