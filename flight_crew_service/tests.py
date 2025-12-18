import time
import concurrent.futures
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import SimpleTestCase, TransactionTestCase
from unittest.mock import MagicMock, patch
from flight_crew_service.models import Pilot, Language

# ==========================================
# 1. BLACK BOX TESTS (Integration)
# ==========================================
class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mert_test",
            password="testpass123"
        )
        self.client.login(username="mert_test", password="testpass123")

class PilotViewSetTest(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        self.list_url = reverse("pilot-list") 

    def test_create_pilot(self):
        payload = {
            "name": "Vecihi Hürkuş",
            "age": 45,
            "gender": "Male",
            "nationality": "TR",
            "seniority_level": "senior",   
            "allowed_range": 5000,         
            "vehicle_restriction": "None"  
        }

        response = self.client.post(self.list_url, payload, format="json")

        if response.status_code != 201:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pilot.objects.count(), 1)
        self.assertEqual(Pilot.objects.get().name, "Vecihi Hürkuş")

    def test_create_pilot_invalid_seniority(self):
        payload = {
            "name": "Invalid Pilot",
            "age": 30,
            "gender": "Male",
            "nationality": "TR",
            "seniority_level": "MegaUltraPilot", 
            "allowed_range": 5000,
            "vehicle_restriction": "None"
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('seniority_level', response.data)

    def test_pilot_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ==========================================
# 2. WHITE BOX TESTS (Unit/Mock)
# ==========================================
class PilotWhiteBoxTest(SimpleTestCase):
    def test_pilot_str_representation_logic(self):
        pilot = Pilot(
            name="Vecihi Hurkus",
            age=45,
            gender="Male",
            nationality="TR",
            seniority_level="senior"
        )
        
        pilot._state = MagicMock()
        pilot._state.db = None

        expected_str = str(pilot)
        self.assertIn("Vecihi Hurkus", expected_str)

    @patch('flight_crew_service.models.Pilot.save')
    def test_pilot_save_mechanism_mock(self, mock_save):
        pilot = Pilot(
            name="Sabiha Gokcen",
            age=35,
            gender="Female",
            nationality="TR",
            seniority_level="senior"
        )
        
        pilot._state = MagicMock()
        pilot._state.db = None

        pilot.save()
        
        self.assertTrue(mock_save.called)

    def test_pilot_seniority_logic_memory(self):
        pilot = Pilot(
            name="Test Pilot",
            seniority_level="junior",
            allowed_range=1000
        )
        
        pilot._state = MagicMock()
        pilot._state.db = None

        self.assertEqual(pilot.allowed_range, 1000)
        self.assertEqual(pilot.seniority_level, "junior")


# ==========================================
# 3. PERFORMANCE TESTS
# ==========================================
class PilotPerformanceTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("pilot-list")

        self.pilots = [
            Pilot(
                name=f"PerfPilot_{i}",
                age=30,
                gender="Male",
                nationality="TR",
                seniority_level="senior",
                allowed_range=5000,
                vehicle_restriction="None"
            )
            for i in range(50)
        ]
        Pilot.objects.bulk_create(self.pilots)

    def test_pilot_list_response_time(self):
        start_time = time.time()

        response = self.client.get(self.url)

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n[Performance] Pilot List API Response Time: {duration:.4f} seconds")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(duration, 0.5)

    def test_pilot_detail_response_time(self):
        pilot = Pilot.objects.first()
        detail_url = reverse("pilot-detail", args=[pilot.pk])

        start_time = time.time()

        response = self.client.get(detail_url)

        end_time = time.time()
        duration = end_time - start_time

        print(f"[Performance] Pilot Detail API Response Time: {duration:.4f} seconds")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(duration, 0.5)

    def test_pilot_create_performance(self):
        payload = {
            "name": "Speedy Gonzales",
            "age": 25,
            "gender": "Male",
            "nationality": "MX",
            "seniority_level": "junior",
            "allowed_range": 3000,
            "vehicle_restriction": "None"
        }

        start_time = time.time()

        response = self.client.post(self.url, payload, format="json")

        end_time = time.time()
        duration = end_time - start_time

        print(f"[Performance] Pilot Creation API Response Time: {duration:.4f} seconds")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(duration, 0.5)


# ==========================================
# 4. LOAD TESTS
# ==========================================
class PilotLoadTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="load_pilot_user",
            password="password123"
        )
        self.url = reverse("pilot-list")

        self.dummy_pilots = [
            Pilot(
                name=f"UpdatePilot_{i}",
                age=30,
                gender="Male",
                nationality="TR",
                seniority_level="junior",
                allowed_range=2000,
                vehicle_restriction="None"
            )
            for i in range(50)
        ]
        Pilot.objects.bulk_create(self.dummy_pilots)
        self.saved_pilots = list(Pilot.objects.all())

    def _generate_create_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)

        payload = {
            "name": f"Load Pilot {index}",
            "age": 30,
            "gender": "Male",
            "nationality": "TR",
            "seniority_level": "junior",
            "allowed_range": 2000,
            "vehicle_restriction": "None"
        }
        
        response = client.post(self.url, payload, format="json")

        if response.status_code != 201:
            print(f"CREATE FAIL: {response.status_code} - {response.data}")

        return response.status_code

    def _generate_read_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        response = client.get(self.url)

        if response.status_code != 200:
            print(f"READ FAIL: {response.status_code}")

        return response.status_code

    def _generate_update_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        pilot = self.saved_pilots[index]
        detail_url = reverse("pilot-detail", args=[pilot.pk])

        payload = {"allowed_range": 9000}

        response = client.patch(detail_url, payload, format="json")

        if response.status_code != 200:
            print(f"UPDATE FAIL: {response.status_code} - {response.data}")

        return response.status_code

    def test_concurrent_pilot_creation_load(self):
        number_of_pilots = 50   
        max_workers = 5

        print(f"\n[Load Test] Starting WRITE attack with {number_of_pilots} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_create_request, range(number_of_pilots)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_201_CREATED)
        fail_count = number_of_pilots - success_count
        rps = number_of_pilots / total_time 

        print(f"[Load Test - Write] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test - Write] Success: {success_count}/{number_of_pilots}")
        print(f"[Load Test - Write] Throughput: {rps:.2f} RPS")

        self.assertEqual(fail_count, 0)

    def test_concurrent_pilot_read_load(self):
        number_of_reads = 50   
        max_workers = 5

        print(f"\n[Load Test] Starting READ attack with {number_of_reads} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_read_request, range(number_of_reads)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_200_OK)
        fail_count = number_of_reads - success_count
        rps = number_of_reads / total_time 

        print(f"[Load Test - Read] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test - Read] Success: {success_count}/{number_of_reads}")
        print(f"[Load Test - Read] Throughput: {rps:.2f} RPS")

        self.assertEqual(fail_count, 0)

    def test_concurrent_pilot_update_load(self):
        number_of_updates = 50   
        max_workers = 5

        print(f"\n[Load Test] Starting UPDATE attack with {number_of_updates} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_update_request, range(number_of_updates)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_200_OK)
        fail_count = number_of_updates - success_count
        rps = number_of_updates / total_time 

        print(f"[Load Test - Update] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test - Update] Success: {success_count}/{number_of_updates}")
        print(f"[Load Test - Update] Throughput: {rps:.2f} RPS")

        self.assertEqual(fail_count, 0)

# ==========================================
# 5. SECURITY TESTS
# ==========================================
class PilotSecurityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sec_pilot", password="password123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("pilot-list")

    def test_negative_age_prevention(self):
        payload = {
            "name": "Benjamin Button",
            "age": -5, 
            "gender": "Male",
            "nationality": "TR",
            "seniority_level": "junior",
            "allowed_range": 5000,
            "vehicle_restriction": "None"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('age', response.data)

    def test_name_length_overflow(self):
        long_name = "A" * 10000 
        payload = {
            "name": long_name,
            "age": 30,
            "gender": "Male",
            "nationality": "TR",
            "seniority_level": "senior",
            "allowed_range": 5000,
            "vehicle_restriction": "None"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

# ==========================================
# 6. ACCEPTANCE TESTS
# ==========================================
class PilotAcceptanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hr_manager", password="password123")
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("pilot-list")

    def test_acceptance_pilot_full_lifecycle(self):
        payload = {
            "name": "Acceptance Pilot",
            "age": 29,
            "gender": "Female",
            "nationality": "TR",
            "seniority_level": "junior",
            "allowed_range": 2000,
            "vehicle_restriction": "None"
        }
        create_resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        pilot_id = create_resp.data["id"]

        list_resp = self.client.get(self.list_url)
        self.assertTrue(any(p["id"] == pilot_id for p in list_resp.data))

        detail_url = reverse("pilot-detail", args=[pilot_id])
        del_resp = self.client.delete(detail_url)
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)

        get_resp = self.client.get(detail_url)
        self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_acceptance_pilot_promotion_workflow(self):
        pilot = Pilot.objects.create(
            name="Junior Pilot",
            age=25,
            gender="Male",
            nationality="TR",
            seniority_level="junior",
            allowed_range=1500,
            vehicle_restriction="None"
        )
        
        detail_url = reverse("pilot-detail", args=[pilot.id])
        promotion_payload = {
            "seniority_level": "senior",
            "allowed_range": 8000
        }
        
        patch_resp = self.client.patch(detail_url, promotion_payload, format="json")
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        
        pilot.refresh_from_db()
        self.assertEqual(pilot.seniority_level, "senior")
        self.assertEqual(pilot.allowed_range, 8000)

    def test_acceptance_pilot_language_certification(self):
        pilot = Pilot.objects.create(
            name="Polyglot Pilot", age=35, seniority_level="senior", allowed_range=5000, vehicle_restriction="None"
        )
        lang = Language.objects.create(language_name="Spanish")
        
        detail_url = reverse("pilot-detail", args=[pilot.id])
        payload = {"languages": [lang.id]}
        
        resp = self.client.patch(detail_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        pilot.refresh_from_db()
        self.assertEqual(pilot.languages.first(), lang)