from parkings.fields import PointField
from parkings.models import Booking, ParkingSpot
from rest_framework import serializers


class ParkingSpotSerializer(serializers.HyperlinkedModelSerializer):
    point = PointField()

    class Meta:
        model = ParkingSpot
        fields = ('url', 'code', 'is_reserved', 'current_base_cost', 'point')


class BookingRequestSerializer(serializers.Serializer):
    from_time = serializers.DateTimeField()
    valid_up_to = serializers.DateTimeField()
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'url',
            'parking_spot',
            'from_time',
            'valid_up_to',
            'total_cost',
            'cancled_at',
        )
