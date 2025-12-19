import time
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from flight_info.flights.models import Airport, VehicleType, Flight
from django.utils import timezone
from datetime import timedelta

class FlightPerformanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="perf_user", password="password123")
        self.client.login(username="perf_user", password="password123")

        self.source = Airport.objects.create(
            country="Turkey", city="Istanbul", name="IST", code="IST"
        )
        self.dest = Airport.objects.create(
            country="UK", city="London", name="Heathrow", code="LHR"
        )
        self.vehicle = VehicleType.objects.create(
            name="Boeing 777", seat_count=300, max_passengers=300
        )

        for i in range(50):
            Flight.objects.create(
                flight_number=f"HB{1000+i}", 
                departure_datetime=timezone.now() + timedelta(days=i),
                duration_minutes=180,
                distance_km=2500,
                source=self.source,
                destination=self.dest,
                vehicle=self.vehicle
            )
        
        self.url = reverse("flight-list")

    def test_flight_list_response_time(self):
        start_time = time.time()
        
        response = self.client.get(self.url)
        
        end_time = time.time()
        duration = end_time - start_time

        print(f"\n[Performance] Flight List API Response Time: {duration:.4f} seconds")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(duration, 0.5)

    def test_flight_creation_performance(self):
        payload = {
            "flight_number": "HB9999", 
            "departure_datetime": (timezone.now() + timedelta(days=5)).isoformat(),
            "duration_minutes": 120,
            "distance_km": 1000,
            "source_airport_code": self.source.code,
            "destination_airport_code": self.dest.code,
            "vehicle_type_model": self.vehicle.name,
            "notes": "Performance test flight"
        }

        start_time = time.time()
        
        response = self.client.post(self.url, payload, format="json")
        
        end_time = time.time()
        duration = end_time - start_time

        print(f"[Performance] Flight Creation API Response Time: {duration:.4f} seconds")

        if response.status_code != 201:
            print(f"ERROR DETAILS: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(duration, 0.5)