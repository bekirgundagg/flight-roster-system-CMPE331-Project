from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from flight_info.flights.models import Airport, VehicleType, Flight


class TestAuthenticatedAPICase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")


class TestAirportViewSet(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport-list")

    def test_create_airport(self):
        payload = {
            "country": "Turkey",
            "city": "Istanbul",
            "name": "Istanbul Airport",
            "code": "IST"
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 1)

    def test_airport_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestVehicleTypeViewSet(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        self.list_url = reverse("vehicletype-list")

    def test_create_vehicle_type(self):
        payload = {
            "name": "A320",
            "seat_count": 180,
            "max_passengers": 170,
            "max_crew": 6
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VehicleType.objects.count(), 1)


class TestFlightViewSet(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()

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

        self.list_url = reverse("flight-list")

    def test_create_flight(self):
        payload = {
            "flight_number": "HB1234",
            "departure_datetime": (timezone.now() + timedelta(days=1)).isoformat(),
            "duration_minutes": 180,
            "distance_km": 2000,
            "source": self.source.id,
            "destination": self.destination.id,
            "vehicle": self.vehicle.id
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 1)

    def test_filter_flight_by_number(self):
        Flight.objects.create(
            flight_number="HB9999",
            departure_datetime=timezone.now(),
            duration_minutes=120,
            distance_km=1000,
            source=self.source,
            destination=self.destination,
            vehicle=self.vehicle
        )

        response = self.client.get(self.list_url, {"flight_number": "HB9999"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
