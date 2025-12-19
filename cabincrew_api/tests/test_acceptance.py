from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from cabincrew_api.models import CabinCrew, Language, VehicleType

class CabinCrewAcceptanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hr_crew_manager", password="password123")
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("cabincrew-list")

        self.lang_eng = Language.objects.create(lan_name="English")
        self.vehicle_b737 = VehicleType.objects.create(type_veh="B737")

    def test_acceptance_recruit_crew_member(self):
        payload = {
            "attendant_id": "CC_ACC_01",
            "name": "New Recruit",
            "age": 22,
            "gender": "Female",
            "nationality": "TR",
            "attendant_type": "regular",
            "seniority_level": "junior",
            "known_languages": [self.lang_eng.id],
            "vehicle_restrictions": [self.vehicle_b737.id]
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        get_response = self.client.get(self.list_url)
        self.assertTrue(any(c["attendant_id"] == "CC_ACC_01" for c in get_response.data))
        
        crew_member = CabinCrew.objects.get(attendant_id="CC_ACC_01")
        self.assertIn(self.lang_eng, crew_member.known_languages.all())

    def test_acceptance_promote_to_chief(self):
        crew = CabinCrew.objects.create(
            attendant_id="CC_ACC_02",
            name="Future Chief",
            age=28,
            gender="Male",
            nationality="TR",
            attendant_type="regular",
            seniority_level="junior"
        )
        
        detail_url = reverse("cabincrew-detail", args=[crew.attendant_id])
        promotion_payload = {
            "attendant_type": "chief",
            "seniority_level": "senior"
        }
        
        response = self.client.patch(detail_url, promotion_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        crew.refresh_from_db()
        self.assertEqual(crew.attendant_type, "chief")
        self.assertEqual(crew.seniority_level, "senior")

    def test_acceptance_resignation_process(self):
        crew = CabinCrew.objects.create(
            attendant_id="CC_ACC_03",
            name="Leaving Staff",
            age=30,
            gender="Female",
            nationality="DE",
            attendant_type="regular",
            seniority_level="senior"
        )
        detail_url = reverse("cabincrew-detail", args=[crew.attendant_id])

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        check_response = self.client.get(detail_url)
        self.assertEqual(check_response.status_code, status.HTTP_404_NOT_FOUND)