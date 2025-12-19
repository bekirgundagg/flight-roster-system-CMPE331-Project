import time
import concurrent.futures
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from flight_info.flights.models import Airport, VehicleType
from django.utils import timezone
from datetime import timedelta

class FlightLoadTest(TransactionTestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="load_flight_user",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("flight-list")

        self.source = Airport.objects.create(
            country="TestCountry", city="LoadCityA", name="Source Airport", code="LSA"
        )
        self.dest = Airport.objects.create(
            country="TestCountry", city="LoadCityB", name="Dest Airport", code="LDB"
        )
        self.vehicle = VehicleType.objects.create(
            name="LoadTestPlane", seat_count=200, max_passengers=200
        )

    def _generate_flight_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)

        flight_number = f"HB{2000 + index}"

        payload = {
            "flight_number": flight_number,
            "departure_datetime": (timezone.now() + timedelta(days=index)).isoformat(),
            "duration_minutes": 150,
            "distance_km": 1200,
            "source_airport_code": self.source.code,
            "destination_airport_code": self.dest.code,
            "vehicle_type_model": self.vehicle.name,
            "notes": f"Load test flight {index}"
        }
        
        response = client.post(self.url, payload, format="json")

        if response.status_code != 201:
            print(f"FAIL [Thread-{index}]: {response.status_code} - {response.data}")

        return response.status_code

    def test_concurrent_flight_creation_load(self):
        number_of_flights = 50   
        max_workers = 5

        print(f"\n[Load Test] Starting flight creation attack with {number_of_flights} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_flight_request, range(number_of_flights)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_201_CREATED)
        fail_count = number_of_flights - success_count
        rps = number_of_flights / total_time 

        print(f"[Load Test] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test] Successful Creations: {success_count}/{number_of_flights}")
        print(f"[Load Test] Throughput: {rps:.2f} requests/second")

        self.assertEqual(fail_count, 0, f"Load test failed. {fail_count} requests dropped.")