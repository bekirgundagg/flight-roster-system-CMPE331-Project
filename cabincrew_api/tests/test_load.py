import time
import concurrent.futures
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from cabincrew_api.models import Language, VehicleType

class CabinCrewLoadTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="load_crew_user",
            password="password123"
        )
        self.url = reverse("cabincrew-list")

        self.language = Language.objects.create(lan_name="LoadTestEnglish")
        self.vehicle = VehicleType.objects.create(
            type_veh="LoadPlane"
        )

    def _generate_crew_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)

        payload = {
            "attendant_id": f"L_CC_{index}",
            "name": f"Load Crew {index}",
            "age": 28,
            "gender": "Female",
            "nationality": "TR",
            "attendant_type": "regular",
            "senority_level": "junior",
            "known_languages": [self.language.id],
            "vehicle_restrictions": [self.vehicle.id]
        }
        
        response = client.post(self.url, payload, format="json")

        if response.status_code != 201:
            print(f"FAIL [Thread-{index}]: {response.status_code} - {response.data}")

        return response.status_code

    def test_concurrent_cabincrew_creation_load(self):
        number_of_crews = 50   
        max_workers = 5

        print(f"\n[Load Test] Starting cabin crew creation attack with {number_of_crews} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_crew_request, range(number_of_crews)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_201_CREATED)
        fail_count = number_of_crews - success_count
        rps = number_of_crews / total_time 

        print(f"[Load Test] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test] Successful Creations: {success_count}/{number_of_crews}")
        print(f"[Load Test] Throughput: {rps:.2f} requests/second")

        self.assertEqual(fail_count, 0)