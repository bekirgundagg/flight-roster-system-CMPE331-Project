from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from django.utils import timezone
from datetime import timedelta
from flight_info.flights.models import Flight, Airport, VehicleType

class FlightWhiteBoxTest(SimpleTestCase):
    def setUp(self):
        self.mock_source = MagicMock(spec=Airport)
        self.mock_source.city = "Istanbul"
        self.mock_source.code = "IST"
        self.mock_source.pk = 1
        self.mock_source._state = MagicMock()
        self.mock_source._state.db = None

        self.mock_dest = MagicMock(spec=Airport)
        self.mock_dest.city = "London"
        self.mock_dest.code = "LHR"
        self.mock_dest.pk = 2
        self.mock_dest._state = MagicMock()
        self.mock_dest._state.db = None

        self.mock_vehicle = MagicMock(spec=VehicleType)
        self.mock_vehicle.name = "Boeing 777"
        self.mock_vehicle.pk = 1
        self.mock_vehicle._state = MagicMock()
        self.mock_vehicle._state.db = None

    def test_flight_str_representation_logic(self):
        flight = Flight(
            flight_number="TK1923",
            source=self.mock_source,
            destination=self.mock_dest,
            vehicle=self.mock_vehicle
        )
        expected_str = str(flight)
        self.assertIn("TK1923", expected_str)

    @patch('flight_info.flights.models.Flight.save')
    def test_flight_save_calls_parent_save(self, mock_save):
        flight = Flight(
            flight_number="MOCK_FLIGHT",
            source=self.mock_source,
            destination=self.mock_dest,
            vehicle=self.mock_vehicle
        )
        flight.save()
        self.assertTrue(mock_save.called)

    def test_flight_duration_logic_memory(self):
        departure = timezone.now()
        flight = Flight(
            flight_number="TEST001",
            departure_datetime=departure,
            duration_minutes=120,
            source=self.mock_source,
            destination=self.mock_dest,
            vehicle=self.mock_vehicle
        )
        arrival_time = flight.departure_datetime + timedelta(minutes=flight.duration_minutes)
        expected_diff = arrival_time - departure
        self.assertEqual(expected_diff.total_seconds(), 7200)