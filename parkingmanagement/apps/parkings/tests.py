import datetime

from django.contrib.auth import get_user_model
from django.contrib.gis import geos as geo_models
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from parkings.exceptions import ParkingSpotNotAvailableError
from parkings.models import Booking, ParkingSpot
from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

USER = get_user_model()
class ParkingSpotTestCase(TestCase):
    def setUp(self):
        ParkingSpot.objects.create(
            code='A', is_reserved=True, point=geo_models.Point(5, 23), current_base_cost=10,
        )
        ParkingSpot.objects.create(
            code='B', is_reserved=False, point=geo_models.Point(5, 29), current_base_cost=20,
        )
        USER.objects.create_user('9657946755','Qwerty@1234')

    def test_available_parking_spot_can_be_booked(self):
        """Test Parking Spot can be booked"""
        obj_code_a_already_reserved = ParkingSpot.objects.get(code='A')
        obj_code_b_not_reserved = ParkingSpot.objects.get(code='B')
        obj_code_b_not_reserved.reserve(from_time=timezone.now(), valid_up_to=timezone.now(), tenant=USER.objects.first())
        assert obj_code_b_not_reserved.is_reserved ==True
        booking_count  = Booking.objects.count()
        assert booking_count == 1


    def test_non_available_parking_spot_can_not_be_booked(self):
        """Test Already Booked Parking Spot can not be booked"""
        obj_code_a_already_reserved = ParkingSpot.objects.get(code='A')
        with self.assertRaises(ParkingSpotNotAvailableError):
            obj_code_a_already_reserved.reserve(
                from_time=timezone.now(), valid_up_to=timezone.now(), tenant=USER.objects.first(),
            )

    def test_relese(self):
        """Test Already Booked Parking Spot can released"""
        obj_code_a_already_reserved = ParkingSpot.objects.get(code='A')
        obj_code_a_already_reserved.release()
        assert obj_code_a_already_reserved.is_reserved == False

    def test_parking_spot_str_is_code(self):
        """Test  Booked Parking Spot str is its code"""
        obj_code_a_already_reserved = ParkingSpot.objects.get(code='A')
        assert str(obj_code_a_already_reserved) == 'A'

    def test_custom_manager_available_returns_only_available(self):
        """Test Spot manager return only available spots"""
        count = ParkingSpot.objects.available().count()
        assert count == 1


class BookingTestCase(TestCase):
    def setUp(self):
        obj_spot = ParkingSpot.objects.create(
            code='A', is_reserved=False, point=geo_models.Point(5, 23), current_base_cost=10,
        )
        USER.objects.create_user('9657946755', 'Qwerty@1234')


    def test_total_cost(self):
        """Test Booking Total coast is minuts * parking spot cost"""
        start_time = timezone.now()
        end_time = timezone.now()+datetime.timedelta(minutes=10)
        booking = ParkingSpot.objects.first().reserve(
            from_time=start_time, valid_up_to=end_time, tenant=USER.objects.first(),
        )

        booking = Booking.objects.first()
        expected = round((end_time - start_time).total_seconds() / 60 * 10,2)
        assert booking.total_cost == expected

    def test_cancel(self):
        """Test Booking Total Cancelation releases the parking spot"""
        start_time = timezone.now()
        end_time = timezone.now()+datetime.timedelta(minutes=10)
        booking = ParkingSpot.objects.first().reserve(
            from_time=start_time, valid_up_to=end_time, tenant=USER.objects.first(),
        )
        booking.cancel()
        assert booking.cancled_at is not None
        assert ParkingSpot.objects.first().is_reserved == False


class ParkingAPITests(APITestCase):
    def setUp(self):
        user = USER.objects.create_user(
            contact_number='lauren', password='Qwerty@1234',
        )
        self.client.login(username='lauren', password='Qwerty@1234')

    def test_parkingspot_list(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('parkingspot-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parkingspot_create(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('parkingspot-list')
        payload = {
            'code': 'D',
            'is_reserved': False,
            'current_base_cost': 10.0,
            'point': {
                'latitude': 49.8782482189424,
                'longitude': 24.452545489,
            },
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('parkingspot-list')
        response = self.client.get(url, format='json')
        assert len(response.data) == 1

    def test_parkingspot_reserve(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('parkingspot-list')
        payload = {
            'code': 'D',
            'is_reserved': False,
            'current_base_cost': 10.0,
            'point': {
                'latitude': 49.8782482189424,
                'longitude': 24.452545489,
            },
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        last_obj = ParkingSpot.objects.last()
        url = reverse('parkingspot-reserve', args=[last_obj.id])
        start_time = timezone.now()
        end_time = timezone.now()+datetime.timedelta(minutes=10)
        payload = {
            'from_time': start_time,
            'valid_up_to': end_time,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('booking-list')
        response = self.client.get(url, format='json')
        assert len(response.data) == 1

    def test_only_available_parkingspot_listing(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('parkingspot-list')
        payload = {
            'code': 'D',
            'is_reserved': False,
            'current_base_cost': 10.0,
            'point': {
                'latitude': 49.8782482189424,
                'longitude': 24.452545489,
            },
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        last_obj = ParkingSpot.objects.last()
        url = reverse('parkingspot-reserve', args=[last_obj.id])
        start_time = timezone.now()
        end_time = timezone.now()+datetime.timedelta(minutes=10)
        payload = {
            'from_time': start_time,
            'valid_up_to': end_time,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('parkingspot-list')
        response = self.client.get(url, format='json')
        assert response.data==[]

    def test_booking_cancel(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('parkingspot-list')
        payload = {
            'code': 'D',
            'is_reserved': False,
            'current_base_cost': 10.0,
            'point': {
                'latitude': 49.8782482189424,
                'longitude': 24.452545489,
            },
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        last_obj = ParkingSpot.objects.last()
        url = reverse('parkingspot-reserve', args=[last_obj.id])
        start_time = timezone.now()
        end_time = timezone.now()+datetime.timedelta(minutes=10)
        payload = {
            'from_time': start_time,
            'valid_up_to': end_time,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('booking-list')
        response = self.client.get(url, format='json')
        url = reverse('booking-cancel', args=[Booking.objects.last().id])
        response = self.client.get(url, {}, format='json')
        assert response.data['cancled_at'] is not None
        url = reverse('booking-list')
        response = self.client.get(url, format='json')
        assert len(response.data) == 0

    def test_parking_spot_filtering(self):
        """
        Ensure we can create a new account object.
        """,
        url = reverse('parkingspot-list')
        dmart_baner = {
            'code': 'D Mart Baner Near Sadanand Hotel, Survey No.110, Baner Road, Laxman Nagar, Baner, Pune, Maharashtra',
            'is_reserved': False,
            'current_base_cost': 10.0,
            'point': {
                'latitude': 18.567124,
                'longitude': 73.769539,
            },
        }
        multifit_baner = {
            'code': 'Pride Gateway, Sr No 112, Opp, D-Mart, Baner road, Pune, Maharashtra 411045',
            'is_reserved': False,
            'current_base_cost': 20.0,
            'point': {
                'latitude': 18.566064,
                'longitude': 73.771443,
            },
        }
        synechron_hinjewadi = {
            'code': 'Synechron Technologies Pvt. Ltd., CEDAR Building Ascendas, Phase 3, Hinjewadi Rajiv Gandhi Infotech Park, Maan, Pune, Maharashtra 411057',
            'is_reserved': False,
            'current_base_cost': 100.0,
            'point': {
                'latitude': 18.595042,
                'longitude': 73.684198,
            },
        }
        response = self.client.post(url, dmart_baner, format='json')
        response = self.client.post(url, multifit_baner, format='json')
        response = self.client.post(url, synechron_hinjewadi, format='json')

        response = self.client.get(
            url, {'lat': '18.570928', 'long': '73.764075','radius': '1000'},
        )
        assert len(response.data) == 2

        response = self.client.get(
            url, {'lat': '18.570928', 'long': '73.764075', 'radius': '10000'},
        )
        assert len(response.data) == 3
