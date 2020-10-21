from parkings.fields import PointField
from parkings.models import Booking, ParkingSpot
from rest_framework import serializers


class ParkingSpotSerializer(serializers.HyperlinkedModelSerializer):
    """
    ParkingSpotSerializer used for Serialization of ParkingSpot Objects.
    """
    point = PointField()
    class Meta:
        model = ParkingSpot
        fields = ('url', 'code', 'is_reserved', 'current_base_cost', 'point')


class BookingRequestSerializer(serializers.Serializer):
    """
    BookingRequestSerializer used for validating
    the request to reserve a ParkingSpot Object.
    """
    from_time = serializers.DateTimeField()
    valid_up_to = serializers.DateTimeField()
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    """
    BookingSerializer used for Serialization of Booking Object.
    """

    class Meta:
        model = Booking
        fields = ('url','parking_spot','from_time','valid_up_to', 'total_cost', 'cancelled_at')
