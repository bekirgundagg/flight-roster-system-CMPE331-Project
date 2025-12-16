from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from flight_crew_service.models import Pilot, Language

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
            print("HATA DETAYI:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Pilot.objects.count(), 1)
        
        self.assertEqual(Pilot.objects.get().name, "Vecihi Hürkuş")

    def test_pilot_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)