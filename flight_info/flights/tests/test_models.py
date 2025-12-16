from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from flight_info.flights.models import (
    Airport,
    VehicleType,
    Flight,
    SharedFlightInfo
)


class TessAirportModel(TestCase):

    def test_create_airport_success(self):
        airport = Airport.objects.create(
            country="Turkey",
            city="Istanbul",
            name="Istanbul Airport",
            code="IST"
        )
        self.assertEqual(str(airport), "IST - Istanbul, Istanbul Airport")

    def test_airport_code_validation(self):
        airport = Airport(
            country="Turkey",
            city="Istanbul",
            name="Invalid Airport",
            code="ist"
        )
        with self.assertRaises(ValidationError):
            airport.full_clean()


class TestVehicleTypeModel(TestCase):

    def test_create_vehicle_type(self):
        vehicle = VehicleType.objects.create(
            name="A320",
            seat_count=180,
            max_passengers=170,
            max_crew=6
        )
        self.assertEqual(str(vehicle), "A320 (180 seats)")

    def test_seat_count_must_be_positive(self):
        vehicle = VehicleType(
            name="Broken Plane",
            seat_count=0,
            max_passengers=100
        )
        with self.assertRaises(ValidationError):
            vehicle.full_clean()


class TestFlightModel(TestCase):

    def setUp(self):
        self.source = Airport.objects.create(
            country="Turkey",
            city="Istanbul",
            name="Istanbul Airport",
            code="IST"
        )
        self.destination = Airport.objects.create(
            country="Germany",
            city="Berlin",
            name="Berlin Airport",
            code="BER"
        )
        self.vehicle = VehicleType.objects.create(
            name="A320",
            seat_count=180,
            max_passengers=170
        )

    def test_create_flight_success(self):
        flight = Flight.objects.create(
            flight_number="HB1234",
            departure_datetime=timezone.now() + timedelta(days=1),
            duration_minutes=180,
            distance_km=2000,
            source=self.source,
            destination=self.destination,
            vehicle=self.vehicle
        )

        self.assertIn("HB1234", str(flight))
        self.assertEqual(flight.source.code, "IST")
        self.assertEqual(flight.destination.code, "BER")

    def test_flight_number_validation(self):
        flight = Flight(
            flight_number="1234HB",
            departure_datetime=timezone.now(),
            duration_minutes=120,
            distance_km=1000,
            source=self.source,
            destination=self.destination,
            vehicle=self.vehicle
        )
        with self.assertRaises(ValidationError):
            flight.full_clean()


class TestSharedFlightInfoModel(TestCase):

    def setUp(self):
        airport1 = Airport.objects.create(
            country="Turkey",
            city="Istanbul",
            name="Istanbul Airport",
            code="IST"
        )
        airport2 = Airport.objects.create(
            country="France",
            city="Paris",
            name="CDG Airport",
            code="CDG"
        )

        vehicle = VehicleType.objects.create(
            name="A320",
            seat_count=180,
            max_passengers=170
        )

        self.flight = Flight.objects.create(
            flight_number="HB5678",
            departure_datetime=timezone.now(),
            duration_minutes=240,
            distance_km=2500,
            source=airport1,
            destination=airport2,
            vehicle=vehicle
        )

    def test_create_shared_flight_info(self):
        shared = SharedFlightInfo.objects.create(
            flight=self.flight,
            partner_airline="Lufthansa",
            partner_flight_number="HB9999"
        )

        self.assertEqual(shared.flight, self.flight)
        self.assertIn("Lufthansa", str(shared))
