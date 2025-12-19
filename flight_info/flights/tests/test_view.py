from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from flight_info.flights.models import Airport, VehicleType, Flight

class FlightViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testpilot", password="password123")
        self.client.login(username="testpilot", password="password123")

        self.source = Airport.objects.create(
            country="Turkey", city="Ankara", name="Esenboga", code="ESB"
        )
        self.dest = Airport.objects.create(
            country="Izmir", city="Izmir", name="Adnan Menderes", code="ADB"
        )
        self.vehicle = VehicleType.objects.create(
            name="Airbus A320", seat_count=180, max_passengers=170
        )

        self.list_url = reverse("flight-list") 

    def test_create_flight_api(self):
        payload = {
            "flight_number": "HB2023",
            "departure_datetime": (timezone.now() + timedelta(days=5)).isoformat(),
            "duration_minutes": 60,
            "distance_km": 600,
            "source_airport_code": self.source.code,
            "destination_airport_code": self.dest.code,
            "vehicle_type_model": self.vehicle.name,
            "notes": "Test flight via API"
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 1)
        self.assertEqual(Flight.objects.get().flight_number, "HB2023")

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
