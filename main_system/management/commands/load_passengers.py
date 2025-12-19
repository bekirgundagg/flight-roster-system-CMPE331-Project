import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
# Passenger modelini import ediyoruz
from passengers.models import Passenger


class Command(BaseCommand):
    help = 'Mevcut Yolcu verilerini TEMİZLER ve JSON dosyasından yeniden yükler'

    def handle(self, *args, **kwargs):
        # Dosya yolunu belirle
        file_path = os.path.join(
            settings.BASE_DIR,
            'main_system', 'management', 'datas', 'passengers.json'
        )

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"HATA: JSON dosyası bulunamadı! Yol: {file_path}"))
            return

        self.stdout.write(f"Dosya okundu: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        try:
            with transaction.atomic():
                self.stdout.write(self.style.WARNING("\n⚠️  Mevcut Yolcular temizleniyor..."))

                # 1. ADIM: SİLME
                count, _ = Passenger.objects.all().delete()
                self.stdout.write(f" - {count} adet yolcu silindi.")
                self.stdout.write(self.style.SUCCESS("✅ Temizlik tamamlandı. Yükleme başlıyor...\n"))

                # 2. ADIM: AYRIŞTIRMA (Yetişkinler vs Bebekler)
                # parent_email alanı dolu olanlar bebektir, boş olanlar yetişkindir.
                adults_data = [p for p in data if not p.get('parent_email')]
                infants_data = [p for p in data if p.get('parent_email')]

                # --- A) Önce Yetişkinleri Yükle ---
                self.stdout.write("--- Yetişkinler Yükleniyor ---")
                for item in adults_data:
                    Passenger.objects.create(
                        first_name=item['first_name'],
                        last_name=item['last_name'],
                        email=item['email'],
                        age=item['age'],
                        gender=item['gender'],
                        nationality=item['nationality'],
                        flight_id=item['flight_id'],
                        seat_type=item['seat_type'],
                        seat_number=item['seat_number'],
                        parent=None  # Yetişkinin ebeveyni yok
                    )
                self.stdout.write(self.style.SUCCESS(f"{len(adults_data)} yetişkin yüklendi."))

                # --- B) Sonra Bebekleri Yükle ve Bağla ---
                self.stdout.write("--- Bebekler Yükleniyor ---")
                for item in infants_data:
                    # Ebeveyni email ile buluyoruz
                    parent_email = item['parent_email']
                    try:
                        parent_obj = Passenger.objects.get(email=parent_email)

                        Passenger.objects.create(
                            first_name=item['first_name'],
                            last_name=item['last_name'],
                            email=item['email'],  # Bebeklerin emaili genelde null olur
                            age=item['age'],
                            gender=item['gender'],
                            nationality=item['nationality'],
                            flight_id=item['flight_id'],
                            seat_type=item['seat_type'],
                            seat_number=item['seat_number'],
                            parent=parent_obj  # <-- İşte ilişki burada kuruluyor
                        )
                        self.stdout.write(f" + Bebek {item['first_name']} (Ebeveyni: {parent_obj.first_name}) eklendi.")

                    except Passenger.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f"HATA: Bebek {item['first_name']} için ebeveyn ({parent_email}) bulunamadı!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ BİR HATA OLUŞTU! HİÇBİR DEĞİŞİKLİK YAPILMADI.\nHata Detayı: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n🚀 İşlem Başarıyla Tamamlandı! Yolcu veritabanı yenilendi."))