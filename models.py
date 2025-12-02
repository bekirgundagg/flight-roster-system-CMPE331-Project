from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

flight_re = RegexValidator(
    regex=r'^HVB\d{3}$',
    message='Flight number must be in AANNNN format (e.g. HVB1234).'
)

airport_code_re = RegexValidator(
    regex=r'^[A-Z]{3}$',
    message='Airport code must be 3 uppercase letters.'
)

SINGLE_AIRLINE_NAME = "HVB Airlines"
SINGLE_AIRLINE_CODE = "HVB"

class Airport(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=3, unique=True, validators=[airport_code_re])

    def __str__(self):
        return f"{self.code} - {self.city}, {self.name}"

class VehicleType(models.Model):
    name = models.CharField(max_length=50)  # e.g. A320
    seat_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seating_plan = models.JSONField(null=True, blank=True)
    max_crew = models.PositiveIntegerField(default=6)
    max_passengers = models.PositiveIntegerField()
    standard_menu = models.JSONField(null=True, blank=True, help_text="Standard menu served on this plane")

    def __str__(self):
        return f"{self.name} ({self.seat_count} seats)"

class Flight(models.Model):
    flight_number = models.CharField(max_length=6, validators=[flight_re])
    departure_datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.PositiveIntegerField()
    source = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="arrivals")
    vehicle = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    # optional: seating map snapshot, other metadata
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [('flight_number')]  # ensure flight numbers unique per airline
        indexes = [
            models.Index(fields=['departure_datetime']),
            models.Index(fields=['flight_number']),
        ]

    def __str__(self):
        return f"{SINGLE_AIRLINE_CODE}{self.flight_number} — {self.source.code}->{self.destination.code} @ {self.departure_datetime}"

class SharedFlightInfo(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE, related_name="shared_info") #her Flight için en fazla bir SharedFlightInfo olabilir.
    partner_airline = models.CharField(max_length=100) 
    partner_flight_number = models.CharField(max_length=6, validators=[flight_re])
    # optionally: connecting flight info for shared flights
    connecting_flight = models.ForeignKey(Flight, null=True, blank=True, on_delete=models.SET_NULL, related_name='connected_to')

    def __str__(self):
        return f"{self.flight} shared with {self.partner_airline}{self.partner_flight_number}"