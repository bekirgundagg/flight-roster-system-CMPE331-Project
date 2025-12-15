from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cabincrew_api.models import CabinCrew, Language
from django.contrib.auth.models import User


class TestCabinCrewViews(APITestCase):

    def setUp(self):
        # user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        # language
        self.language = Language.objects.create(lan_name="English")

        # cabin crew
        self.crew = CabinCrew.objects.create(
            attendant_id="CC100",
            name="John",
            age=30,
            gender="Male",
            nationality="US",
            attendant_type="regular",
            seniority_level="junior",
        )

        self.crew.known_languages.add(self.language)

        self.list_url = reverse("cabincrew-list")
        self.detail_url = reverse("cabincrew-detail", args=[self.crew.pk])

    def test_create_cabincrew_with_missing_field_fails(self):
        invalid_payload = {
            "attendant_id": "CC201",
            "name": "Alex",
            "age": 25,
            "nationality": "DE",
            "attendant_type": "crew",
            "seniority_level": "junior",
        }

        response = self.client.post(self.list_url, invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("gender", response.data)

    def test_update_cabincrew_age(self):
        update_payload = {
            "attendant_id": self.crew.attendant_id,
            "name": self.crew.name,
            "age": 35,
            "gender": self.crew.gender,
            "nationality": self.crew.nationality,
            "attendant_type": self.crew.attendant_type,
            "seniority_level": "senior",
            "known_languages": [self.language.id], 
        }

        response = self.client.patch(self.detail_url, update_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["age"], 35)

        self.crew.refresh_from_db()
        self.assertEqual(self.crew.age, 35)

    def test_delete_cabincrew(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CabinCrew.objects.count(), 0)
