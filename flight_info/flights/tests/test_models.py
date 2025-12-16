from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from flight_info.flights.models import Flight, Airport, VehicleType

class FlightModelTest(TestCase):
    def setUp(self):
        self.source = Airport.objects.create(
            country="Turkey", city="Istanbul", name="Sabiha Gokcen", code="SAW"
        )
        self.destination = Airport.objects.create(
            country="Germany", city="Berlin", name="Berlin Airport", code="BER"
        )
        self.vehicle = VehicleType.objects.create(
            name="Boeing 737", seat_count=189, max_passengers=180
        )

    def test_create_valid_flight(self):
        flight = Flight(
            flight_number="HB1071",
            departure_datetime=timezone.now() + timedelta(days=1),
            duration_minutes=120,
            distance_km=1500,
            source=self.source,
            destination=self.destination,
            vehicle=self.vehicle
        )
        try:
            flight.full_clean()
            flight.save()
        except ValidationError:
            self.fail("ValidationError !")

    def test_invalid_flight_number_regex(self):
        flight = Flight(
            flight_number="XY1234",  
            departure_datetime=timezone.now(),
            duration_minutes=120,
            distance_km=1500,
            source=self.source,
            destination=self.destination,
            vehicle=self.vehicle
        )
        with self.assertRaises(ValidationError):
            flight.full_clean()

    def test_airport_code_length(self):
        airport = Airport(
            country="Turkey", city="Antalya", name="Antalya Airport", 
            code="AYTXXXX" 
        )
        with self.assertRaises(ValidationError):
            airport.full_clean()
