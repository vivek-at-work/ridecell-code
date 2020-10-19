from parkings.exceptions import (NotAvailableToCancelError,
                                 ParkingSpotNotAvailableError)
from parkings.filters import DistanceToPointFilter
from parkings.models import Booking, ParkingSpot
from parkings.serializers import (BookingRequestSerializer, BookingSerializer,
                                  ParkingSpotSerializer)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ParkingSpotViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSpotSerializer
    queryset = ParkingSpot.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DistanceToPointFilter,)

    @action(
        detail=True,
        serializer_class=BookingRequestSerializer,
        permission_classes=[permissions.IsAuthenticated],
        methods=['post'],
    )
    def reserve(self, request, pk=None):
        serializer = self.serializer_class(
            data=request.data, context={'request': request},
        )
        if serializer.is_valid(raise_exception=True):
            parking_spot = self.get_object()
            try:
                booking = parking_spot.reserve(**serializer.validated_data)
                parking_spot.save()
                return Response(
                    BookingSerializer(booking, context={'request': request}).data,
                    status=status.HTTP_201_CREATED,
                )
            except ParkingSpotNotAvailableError as err:
                return Response(
                    {'message':str(err)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def get_queryset(self):
        return ParkingSpot.objects.available()


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            booking = self.get_object()
            booking.cancel()
            booking.save()
            return Response(
                self.serializer_class(booking, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
        except NotAvailableToCancelError as err:
            return Response(
                {'message':str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.bookings.current()
        return Booking.objects.none()
