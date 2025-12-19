from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from cabincrew_api.models import Language, VehicleType

class CabinCrewSecurityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sec_crew_user",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("cabincrew-list")

        self.language = Language.objects.create(lan_name="SecLang")
        self.vehicle = VehicleType.objects.create(type_veh="SecPlane")

    def test_prevent_negative_age(self):
        payload = {
            "attendant_id": "CC_SEC_01",
            "name": "Benjamin Button",
            "age": -10,
            "gender": "Male",
            "nationality": "TR",
            "attendant_type": "regular",
            "seniority_level": "junior",
            "known_languages": [self.language.id],
            "vehicle_restrictions": [self.vehicle.id]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('age', response.data)

    def test_prevent_name_buffer_overflow(self):
        long_name = "A" * 5000
        
        payload = {
            "attendant_id": "CC_SEC_02",
            "name": long_name,
            "age": 25,
            "gender": "Female",
            "nationality": "TR",
            "attendant_type": "regular",
            "seniority_level": "junior",
            "known_languages": [self.language.id],
            "vehicle_restrictions": [self.vehicle.id]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)