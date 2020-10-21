class ParkingSpotNotAvailableError(Exception):
    """Exception raised while trying to book a already reserved parking spot.

    Attributes:
        parking_spot -- input parking spot which caused the error
    """

    def __init__(self, parking_spot, message='Parking Spot is not available.'):
        self.parking_spot = parking_spot
        self.message = message
        super().__init__(self.message)


class NotAvailableToCancelError(Exception):
    """Exception raised while trying to cancel an already cancelled booking.

    Attributes:
        booking -- input booking which caused the error.
    """

    def __init__(self, booking, message='Booking Spot is not available for Cancelation.'):
        self.booking = booking
        self.message = message
        super().__init__(self.message)
