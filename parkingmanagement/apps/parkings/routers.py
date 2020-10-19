from parkings.views import BookingViewSet, ParkingSpotViewSet
from rest_framework.routers import DefaultRouter

parkings_router = DefaultRouter()
parkings_router.register(r'parkings', ParkingSpotViewSet)
parkings_router.register(r'bookings', BookingViewSet)
