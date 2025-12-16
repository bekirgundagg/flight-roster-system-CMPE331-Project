# passengers/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Passenger

class PassengerViewSetTest(APITestCase):

    def setUp(self):
        # 1. Test Kullanıcısı Oluştur
        self.user = User.objects.create_user(
            username="test_user",
            password="testpassword123"
        )
        
        # 2. Token/Auth İşlemi (Zorla giriş yap)
        self.client.force_authenticate(user=self.user)

        # 3. URL Tanımı
        self.list_url = reverse("passenger-list") 

    # --- TEST 1: Standart Yolcu ---
    def test_create_standard_passenger(self):
        """
        1. Standart bir yetişkin yolcu oluşturma testi.
        """
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

    # --- TEST 2: Bebek ve Ebeveyn ---
    def test_create_infant_passenger(self):
        """
        2. Önce ebeveyn, sonra bebek yolcu oluşturma testi.
        """
        # Önce Ebeveyni Oluştur
        parent = Passenger.objects.create(
            first_name="Anne",
            last_name="Yilmaz",
            flight_id="TK1903",
            age=30,
            gender="F",
            nationality="TR",
            seat_type="economy"
        )

        # [cite_start]Bebek için payload (0-2 yaş kuralı [cite: 72])
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
        
        # İlişkiyi kontrol et
        infant = Passenger.objects.get(first_name="Bebek")
        self.assertEqual(infant.parent, parent)

    # --- TEST 3: Yetkisiz Erişim ---
    def test_auth_required(self):
        """
        3. Giriş yapmamış kullanıcı erişememeli.
        """
        self.client.force_authenticate(user=None) # Çıkış yap
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- TEST 4: E-posta Benzersizliği (Unique Constraints) ---
    def test_create_passenger_unique_email(self):
        """
        4. Aynı e-posta adresiyle ikinci bir yolcu oluşturulmamalı.
        """
        # İlk yolcuyu oluştur (manuel db kaydı)
        Passenger.objects.create(
            first_name="Ahmet",
            last_name="Demir",
            email="ayni@mail.com", # <--- Bu mail kullanıldı
            age=30,
            flight_id="TK100",
            gender="M"
        )

        # Aynı mail ile API üzerinden ikinci yolcuyu eklemeye çalış
        payload = {
            "first_name": "Mehmet",
            "last_name": "Demir",
            "email": "ayni@mail.com", # <--- AYNI MAIL! Hata vermeli.
            "age": 40,
            "gender": "M",
            "nationality": "TR",
            "flight_id": "TK101",
            "seat_type": "business"
        }

        response = self.client.post(self.list_url, payload, format="json")

        # 400 BAD REQUEST bekliyoruz çünkü unique constraint ihlali var
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Hatanın email alanında olduğunu doğrula
        self.assertIn('email', response.data)

    # --- TEST 5: Geçersiz Seçenek (Invalid Choice) ---
    def test_create_passenger_invalid_choice(self):
        """
        5. Tanımlı olmayan bir cinsiyet veya koltuk tipi girilirse reddedilmeli.
        """
        payload = {
            "first_name": "Yanlis",
            "last_name": "Veri",
            "age": 25,
            "gender": "X",          # <--- 'X' diye bir cinsiyet tanımlamadın (Sadece M, F, O)
            "nationality": "TR",
            "flight_id": "TK999",
            "seat_type": "camping", # <--- 'camping' diye bir koltuk tipi yok
        }

        response = self.client.post(self.list_url, payload, format="json")

        # 400 BAD REQUEST bekliyoruz
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Hangi alanların hata verdiğini kontrol et
        self.assertIn('gender', response.data)
        self.assertIn('seat_type', response.data)