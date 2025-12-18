from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from flight_info.flights.models import Airport, VehicleType, Flight

class FlightAcceptanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="acc_manager", password="password123")
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("flight-list")

        self.source = Airport.objects.create(country="TR", city="Istanbul", name="IST", code="IST")
        self.dest = Airport.objects.create(country="DE", city="Berlin", name="BER", code="BER")
        self.vehicle = VehicleType.objects.create(name="Boeing 737", seat_count=180, max_passengers=180)

    def test_acceptance_create_and_retrieve_flight_lifecycle(self):
        flight_payload = {
            "flight_number": "HB2025",
            "departure_datetime": (timezone.now() + timedelta(days=1)).isoformat(),
            "duration_minutes": 180,
            "distance_km": 2000,
            "source": self.source.id,
            "destination": self.dest.id,
            "vehicle": self.vehicle.id,
            "notes": "Acceptance Test Flight"
        }

        create_response = self.client.post(self.list_url, flight_payload, format="json")
        
        if create_response.status_code != 201:
            print(f"\n[DEBUG] Lifecycle Create Fail: {create_response.data}")

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        created_id = create_response.data["id"]

        get_response = self.client.get(self.list_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        
        flight_exists = any(f["id"] == created_id for f in get_response.data)
        self.assertTrue(flight_exists)

    def test_acceptance_prevent_duplicate_flight_numbers(self):
        Flight.objects.create(
            flight_number="HB9000", 
            departure_datetime=timezone.now(),
            duration_minutes=100,
            distance_km=500,
            source=self.source,
            destination=self.dest,
            vehicle=self.vehicle
        )

        payload = {
            "flight_number": "HB9000",
            "departure_datetime": (timezone.now() + timedelta(days=1)).isoformat(),
            "duration_minutes": 100,
            "distance_km": 500,
            "source": self.source.id,
            "destination": self.dest.id,
            "vehicle": self.vehicle.id
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_acceptance_update_flight_schedule_workflow(self):
        flight = Flight.objects.create(
            flight_number="HB9001", 
            departure_datetime=timezone.now(),
            duration_minutes=100,
            distance_km=500,
            source=self.source,
            destination=self.dest,
            vehicle=self.vehicle
        )

        detail_url = reverse("flight-detail", args=[flight.id])
        
        new_time = (timezone.now() + timedelta(days=5)).isoformat()
        patch_payload = {"departure_datetime": new_time}

        response = self.client.patch(detail_url, patch_payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_time = response.data["departure_datetime"]
        self.assertTrue(new_time.split("T")[0] in response_time)