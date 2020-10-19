from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geo_models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parkings.exceptions import ParkingSpotNotAvailableError

USER = get_user_model()

class ParkingSpotQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_reserved=False)


class ParkingSpot(models.Model):
    """
    An Parking Spot that is registered to the system for further bookings.
    """

    code = models.CharField(
        max_length=256, help_text=_('Human readable name/code'),
    )
    is_reserved = models.BooleanField(default=False)
    point = geo_models.PointField(
        geography=True,
            help_text=_('Represented as (longitude, latitude)'),
    )
    current_base_cost = models.FloatField(
        help_text=_('Price for the parking spot per minute'),
    )
    objects = ParkingSpotQuerySet.as_manager()

    def reserve(self, **kwargs):
        """"Reserve this parking and  create booking object

        Raises:
            ParkingSpotNotAvailableError: raises exception if trying to book already booked parking.

        Returns:
            Booking: A Booking object with booking details.
        """
        if self.is_reserved:
            raise ParkingSpotNotAvailableError(self)
        self.is_reserved = True
        kwargs.update(
            {'applicable_base_cost': self.current_base_cost, 'parking_spot': self},
        )
        return Booking.objects.create(**kwargs)

    def release(self, **kwargs):
        """"Release this parking object
        Returns:
            Booking: A Booking object with booking details.
        """
        self.is_reserved = False

    def __str__(self):
        return '%s' % (self.code)


class Booking(models.Model):
    """
    An Parking Spot that is registered to the system for further bookings.
    """

    parking_spot = models.ForeignKey(
        ParkingSpot,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text=_('Parking Spot for which booking is Created.'),
    )
    from_time = models.DateTimeField(
        help_text=_('from what time this booking is valid.'),
    )
    valid_up_to = models.DateTimeField(
        help_text=_('till what time this booking is valid.'),
    )
    tenant = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text=_('User for whom booking is Created.'),
    )
    cancled_at = models.DateTimeField(
        blank=True, null=True, help_text=_('Till what time this booking is valid.'),
    )

    applicable_base_cost = models.FloatField(
        blank=True, null=True, help_text=_('Cost at which the booking was done.'),
    )

    @property
    def total_cost(self):
        """total cost applicable for this booking

        Returns:
            float: total cost applicable
        """
        from_time = self.from_time
        valid_up_to = self.valid_up_to
        return (
            (valid_up_to - from_time).total_seconds() /
            60 * self.applicable_base_cost
        )

    def cancel(self):
        """
        Cancles this booking and releses the parking spot
        """
        self.cancled_at = timezone.now()
        self.parking_spot.release()
        self.parking_spot.save()

    def __str__(self):
        return f'{self.parking_spot} - {self.from_time} - {self.valid_up_to}'
