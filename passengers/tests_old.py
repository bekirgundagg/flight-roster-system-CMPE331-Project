import time
import concurrent.futures
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TransactionTestCase
from unittest.mock import MagicMock, patch
from passengers.models import Passenger

# ==========================================
# 1. BLACK BOX TESTS (Integration)
# ==========================================
class PassengerViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("passenger-list") 

    def test_create_standard_passenger(self):
        payload = {
            "first_name": "Mert",
            "last_name": "Yilmaz",
            "email": "mert@test.com",
            "age": 25,
            "gender": "M",
            "nationality": "TR",
            "flight_id": "TK1903",
            "seat_type": "economy",
            "seat_number": "12A"
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Passenger.objects.count(), 1)

    def test_create_infant_passenger(self):
        parent = Passenger.objects.create(
            first_name="Anne",
            last_name="Yilmaz",
            flight_id="TK1903",
            age=30,
            gender="F",
            nationality="TR",
            seat_type="economy"
        )

        infant_payload = {
            "first_name": "Bebek",
            "last_name": "Yilmaz",
            "age": 1,
            "gender": "M",
            "nationality": "TR",
            "flight_id": "TK1903",
            "seat_type": "economy",
            "parent": parent.id
        }

        response = self.client.post(self.list_url, infant_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        infant = Passenger.objects.get(first_name="Bebek")
        self.assertEqual(infant.parent, parent)

    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_passenger_unique_email(self):
        Passenger.objects.create(
            first_name="Ahmet",
            last_name="Demir",
            email="ayni@mail.com",
            age=30,
            flight_id="TK100",
            gender="M"
        )

        payload = {
            "first_name": "Mehmet",
            "last_name": "Demir",
            "email": "ayni@mail.com", 
            "age": 40,
            "gender": "M",
            "nationality": "TR",
            "flight_id": "TK101",
            "seat_type": "business"
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_passenger_invalid_choice(self):
        payload = {
            "first_name": "Yanlis",
            "last_name": "Veri",
            "age": 25,
            "gender": "X",        
            "nationality": "TR",
            "flight_id": "TK999",
            "seat_type": "camping", 
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('gender', response.data)
        self.assertIn('seat_type', response.data)


# ==========================================
# 2. WHITE BOX TESTS (Unit/Mock)
# ==========================================
class PassengerWhiteBoxTest(SimpleTestCase):
    def test_passenger_str_representation_memory(self):
        passenger = Passenger(
            first_name="Mert",
            last_name="Yilmaz",
            email="mert@test.com",
            age=25,
            gender="M",
            nationality="TR",
            seat_type="economy"
        )
        
        passenger._state = MagicMock()
        passenger._state.db = None

        expected_str = str(passenger)
        self.assertIn("Mert", expected_str)
        self.assertIn("Yilmaz", expected_str)

    @patch('passengers.models.Passenger.save')
    def test_passenger_save_mechanism_mock(self, mock_save):
        passenger = Passenger(
            first_name="Test",
            last_name="User",
            email="test@user.com",
            age=30,
            gender="F"
        )
        
        passenger._state = MagicMock()
        passenger._state.db = None

        passenger.save()
        
        self.assertTrue(mock_save.called)

    def test_infant_parent_relation_memory(self):
        parent = Passenger(
            first_name="Mother",
            last_name="Doe",
            age=30
        )
        # Mocking the state AND the fields cache specifically
        parent._state = MagicMock()
        parent._state.db = None
        parent._state.fields_cache = {}

        infant = Passenger(
            first_name="Baby",
            last_name="Doe",
            age=1,
            parent=parent
        )
        infant._state = MagicMock()
        infant._state.db = None
        infant._state.fields_cache = {}

        # Manually assign parent logic
        infant.parent = parent

        self.assertEqual(infant.parent, parent)
        self.assertEqual(infant.parent.first_name, "Mother")


# ==========================================
# 3. PERFORMANCE TESTS
# ==========================================
class PassengerPerformanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="perf_pass_user",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("passenger-list")

        # Create 50 dummy passengers for list performance
        passengers = [
            Passenger(
                first_name=f"PerfName{i}",
                last_name=f"PerfSurname{i}",
                email=f"perf{i}@test.com", # Unique emails
                age=20 + (i % 30),
                gender="M",
                nationality="TR",
                flight_id=f"TK{1000+i}",
                seat_type="economy"
            )
            for i in range(50)
        ]
        Passenger.objects.bulk_create(passengers)

    def test_passenger_list_response_time(self):
        start_time = time.time()

        response = self.client.get(self.url)

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n[Performance] Passenger List API Response Time: {duration:.4f} seconds")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(duration, 0.5)

    def test_passenger_create_performance(self):
        payload = {
            "first_name": "Flash",
            "last_name": "Gordon",
            "email": "speed@test.com",
            "age": 30,
            "gender": "M",
            "nationality": "USA",
            "flight_id": "TK9999",
            "seat_type": "business"
        }

        start_time = time.time()

        response = self.client.post(self.url, payload, format="json")

        end_time = time.time()
        duration = end_time - start_time

        print(f"[Performance] Passenger Creation API Response Time: {duration:.4f} seconds")

        if response.status_code != 201:
            print(f"ERROR DETAILS: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(duration, 0.5)


# ==========================================
# 4. LOAD TESTS
# ==========================================
class PassengerLoadTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="load_pass_user",
            password="password123"
        )
        self.url = reverse("passenger-list")
        
        self.parent = Passenger.objects.create(
            first_name="Parent",
            last_name="Load",
            email="parent@load.com",
            age=35,
            gender="F",
            nationality="US",
            flight_id="TK_LOAD",
            seat_type="economy"
        )

        dummy_passengers = [
            Passenger(
                first_name=f"ReadUser{i}",
                last_name="Read",
                email=f"read{i}@test.com",
                age=25,
                flight_id="TK_READ",
                seat_type="economy"
            )
            for i in range(50)
        ]
        Passenger.objects.bulk_create(dummy_passengers)

    def _generate_create_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)

        payload = {
            "first_name": f"LoadUser{index}",
            "last_name": "Test",
            "email": f"write{index}@test.com",
            "age": 25,
            "gender": "M",
            "nationality": "TR",
            "flight_id": "TK_WRITE",
            "seat_type": "economy",
            "seat_number": "12A"
        }
        
        response = client.post(self.url, payload, format="json")

        if response.status_code != 201:
            print(f"CREATE FAIL [Thread-{index}]: {response.status_code} - {response.data}")

        return response.status_code

    def _generate_read_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        response = client.get(self.url)

        if response.status_code != 200:
            print(f"READ FAIL [Thread-{index}]: {response.status_code}")

        return response.status_code

    def _generate_infant_request(self, index):
        client = APIClient()
        client.force_authenticate(user=self.user)

        payload = {
            "first_name": f"Infant{index}",
            "last_name": "Load",
            "age": 1,
            "gender": "F",
            "nationality": "US",
            "flight_id": "TK_LOAD",
            "seat_type": "economy",
            "parent": self.parent.id
        }

        response = client.post(self.url, payload, format="json")

        if response.status_code != 201:
            print(f"INFANT FAIL [Thread-{index}]: {response.status_code} - {response.data}")
            
        return response.status_code

    def test_concurrent_passenger_creation_load(self):
        number_of_users = 50   
        max_workers = 5       

        print(f"\n[Load Test] Starting WRITE attack with {number_of_users} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_create_request, range(number_of_users)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_201_CREATED)
        fail_count = number_of_users - success_count
        rps = number_of_users / total_time 

        print(f"[Load Test - Write] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test - Write] Success: {success_count}/{number_of_users}")
        print(f"[Load Test - Write] Throughput: {rps:.2f} RPS")

        self.assertEqual(fail_count, 0)

    def test_concurrent_passenger_read_load(self):
        number_of_reads = 100   
        max_workers = 10       

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

    def test_concurrent_infant_assignment_load(self):
        number_of_infants = 30   
        max_workers = 5       

        print(f"\n[Load Test] Starting RELATIONAL (Infant) attack with {number_of_infants} requests...")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._generate_infant_request, range(number_of_infants)))

        end_time = time.time()
        total_time = end_time - start_time

        success_count = results.count(status.HTTP_201_CREATED)
        fail_count = number_of_infants - success_count
        rps = number_of_infants / total_time 

        print(f"[Load Test - Relation] Finished in {total_time:.4f} seconds.")
        print(f"[Load Test - Relation] Success: {success_count}/{number_of_infants}")
        print(f"[Load Test - Relation] Throughput: {rps:.2f} RPS")

        self.assertEqual(fail_count, 0)


# ==========================================
# 5. SECURITY TESTS
# ==========================================
class PassengerSecurityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sec_pass", password="password123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("passenger-list")

    def test_negative_age_prevention(self):
        payload = {
            "first_name": "Benjamin",
            "last_name": "Button",
            "email": "benjamin@test.com",
            "age": -5,
            "gender": "M",
            "nationality": "US",
            "flight_id": "TK_SEC",
            "seat_type": "economy"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('age', response.data)

    def test_name_length_overflow(self):
        long_name = "A" * 10000 
        payload = {
            "first_name": long_name,
            "last_name": "Overflow",
            "email": "overflow@test.com",
            "age": 25,
            "gender": "M",
            "nationality": "US",
            "flight_id": "TK_SEC",
            "seat_type": "economy"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

# ==========================================
# 6. ACCEPTANCE TESTS
# ==========================================
class PassengerAcceptanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ground_ops", password="password123")
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("passenger-list")

    def test_acceptance_vip_family_trip_flow(self):
        parent_payload = {
            "first_name": "VIP",
            "last_name": "Father",
            "email": "vip.father@test.com",
            "age": 40,
            "gender": "M",
            "nationality": "TR",
            "flight_id": "TK_VIP_01",
            "seat_type": "business",
            "seat_number": "1A"
        }
        parent_resp = self.client.post(self.list_url, parent_payload, format="json")
        self.assertEqual(parent_resp.status_code, status.HTTP_201_CREATED)
        parent_id = parent_resp.data["id"]

        infant_payload = {
            "first_name": "VIP",
            "last_name": "Baby",
            "age": 1,
            "gender": "F",
            "nationality": "TR",
            "flight_id": "TK_VIP_01",
            "seat_type": "business",
            "parent": parent_id
        }
        infant_resp = self.client.post(self.list_url, infant_payload, format="json")
        self.assertEqual(infant_resp.status_code, status.HTTP_201_CREATED)

        infant = Passenger.objects.get(id=infant_resp.data["id"])
        self.assertEqual(infant.parent.id, parent_id)
        self.assertTrue(infant.is_infant)

    def test_acceptance_change_seat_assignment(self):
        p = Passenger.objects.create(
            first_name="Seat", last_name="Changer", email="seat@test.com", 
            flight_id="TK_SEAT", seat_type="economy", seat_number="20D"
        )

        detail_url = reverse("passenger-detail", args=[p.id])
        payload = {"seat_number": "15F"}
        
        resp = self.client.patch(detail_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        p.refresh_from_db()
        self.assertEqual(p.seat_number, "15F")

    def test_acceptance_duplicate_email_prevention_flow(self):

        Passenger.objects.create(
            first_name="Original", last_name="User", email="unique@test.com", 
            flight_id="TK_UNIQ", seat_type="economy"
        )

        payload = {
            "first_name": "Imposter",
            "last_name": "User",
            "email": "unique@test.com", 
            "age": 30,
            "gender": "M",
            "nationality": "US",
            "flight_id": "TK_UNIQ",
            "seat_type": "economy"
        }

        resp = self.client.post(self.list_url, payload, format="json")
        
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", resp.data)