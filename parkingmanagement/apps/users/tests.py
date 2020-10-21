from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .backends import ConatctNumberBasedAuthenticationsBackend

USER = get_user_model()
CONTACT_NUMBER = '9657946755'
PASSWORD ='Qwerty@1234'


class UsersTestCase(TestCase):
    def test_normal_user_creation(self):
        """Test Normal User Creation"""
        u = USER.objects.create_user(CONTACT_NUMBER, PASSWORD)
        assert u.contact_number == CONTACT_NUMBER
        assert u.is_staff == True
        assert u.is_superuser == False
        assert u.has_perm('', None) == False
        assert u.has_module_perms('') == False


    def test_super_user_creation(self):
        """Test Super User Creation"""
        u = USER.objects.create_superuser(CONTACT_NUMBER, PASSWORD)
        assert u.contact_number == CONTACT_NUMBER
        assert u.is_staff == True
        assert u.is_superuser == True
        assert u.has_perm('', None) == True
        assert u.has_module_perms('') == True
        assert str(u) == u.contact_number


class ConatctNumberBasedAuthenticationsBackendTestCase(TestCase):
    def setUp(self):
        USER.objects.create_user(CONTACT_NUMBER, PASSWORD)

    def test_user_login(self):
        """Test Existing User can login"""
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=CONTACT_NUMBER, password=PASSWORD,
        )
        assert str(t) == CONTACT_NUMBER

    def test_non_user_login(self):
        """Test Non Existing User User Login"""
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=CONTACT_NUMBER[::-1], password=PASSWORD,
        )
        assert t is None


class UsersAPITests(APITestCase):
    def test_user_sign_up(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user-signup')
        payload = {
            'contact_number': CONTACT_NUMBER,
            'password': PASSWORD,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=CONTACT_NUMBER, password=PASSWORD,
        )
        assert str(t) == CONTACT_NUMBER


    def test_user_list(self):
        """
        Ensure we can create a new user object and get the same in list.
        """
        sign_up_url = reverse('user-signup')
        payload = {
            'contact_number': CONTACT_NUMBER,
            'password': PASSWORD,
        }
        sign_up_response = self.client.post(sign_up_url, payload, format='json')
        self.assertEqual(sign_up_response.status_code, status.HTTP_201_CREATED)
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=CONTACT_NUMBER, password=PASSWORD,
        )
        self.client.login(username=CONTACT_NUMBER, password=PASSWORD)
        list_url = reverse('user-list')
        list_response = self.client.get(list_url, format='json')
        assert len(list_response.data) == 1

    def test_duplicate_user_sign_up(self):
        """
        Ensure we can register a new user object with a unique  contact number
        once only
        """
        sign_up_url = reverse('user-signup')
        payload = {
            'contact_number': CONTACT_NUMBER,
            'password': PASSWORD,
        }
        sign_up_response = self.client.post(sign_up_url, payload, format='json')
        self.assertEqual(sign_up_response.status_code, status.HTTP_201_CREATED)
        duplicate_sign_up_response = self.client.post(sign_up_url, payload, format='json')
        self.assertEqual(duplicate_sign_up_response.status_code, status.HTTP_400_BAD_REQUEST)
