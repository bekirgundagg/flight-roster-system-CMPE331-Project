from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from flight_info.flights.models import Airport, VehicleType
from django.utils import timezone
from datetime import timedelta

class FlightSecurityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sec_user", password="password123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("flight-list")

        self.source = Airport.objects.create(
            country="Turkey", city="Istanbul", name="IST", code="IST"
        )
        self.dest = Airport.objects.create(
            country="UK", city="London", name="Heathrow", code="LHR"
        )
        self.vehicle = VehicleType.objects.create(
            name="SecurityPlane", seat_count=100, max_passengers=100
        )

    def test_flight_number_injection_protection(self):
        malicious_payload = {
            "flight_number": "HB1000' OR '1'='1", 
            "departure_datetime": (timezone.now() + timedelta(days=1)).isoformat(),
            "duration_minutes": 120,
            "distance_km": 1000,
            "source": self.source.id,
            "destination": self.dest.id,
            "vehicle": self.vehicle.id
        }

        response = self.client.post(self.url, malicious_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('flight_number', response.data)

    def test_api_date_parsing_resilience(self):
        invalid_payload = {
            "flight_number": "HB2024",
            "departure_datetime": "THIS_IS_NOT_A_DATE_DROP_TABLE",
            "duration_minutes": 120,
            "distance_km": 1000,
            "source": self.source.id,
            "destination": self.dest.id,
            "vehicle": self.vehicle.id
        }

        response = self.client.post(self.url, invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('departure_datetime', response.data)