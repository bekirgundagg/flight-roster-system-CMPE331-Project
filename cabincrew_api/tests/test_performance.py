import time
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from cabincrew_api.models import CabinCrew, Language, VehicleType

class CabinCrewPerformanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="perf_crew_user",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("cabincrew-list")

        crews = [
            CabinCrew(
                attendant_id=f"CCPERF{i}",
                name=f"Crew Member {i}",
                age=25,
                gender="Female",
                nationality="TR",
                attendant_type="regular",
                senority_level="junior"
            )
            for i in range(50)
        ]
        CabinCrew.objects.bulk_create(crews)

    def test_cabincrew_list_response_time(self):
        start_time = time.time()

        response = self.client.get(self.url)

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n[Performance] CabinCrew List API Response Time: {duration:.4f} seconds")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(duration, 0.5)

    def test_cabincrew_create_performance(self):
        v_type = VehicleType.objects.create(
            type_veh="B737"
        )

        payload = {
            "attendant_id": "CC_NEW_01",
            "name": "Performance Check",
            "age": 30,
            "gender": "Male",
            "nationality": "US",
            "attendant_type": "chief",
            "senority_level": "senior",
            "vehicle_restrictions": [v_type.id]
        }

        start_time = time.time()

        response = self.client.post(self.url, payload, format="json")

        end_time = time.time()
        duration = end_time - start_time

        print(f"[Performance] CabinCrew Creation API Response Time: {duration:.4f} seconds")

        if response.status_code != 201:
            print(f"ERROR DETAILS: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(duration, 0.5)