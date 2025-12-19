import json
import os
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.db import transaction  # <-- Veri güvenliği için bunu ekledik
from flight_info.flights.models import Flight, VehicleType, Airport


class Command(BaseCommand):
    help = 'Mevcut verileri TEMİZLER ve JSON dosyasından yeniden yükler'

    def handle(self, *args, **kwargs):
        # Dosya yolunu belirle
        file_path = os.path.join(
            settings.BASE_DIR,
            'main_system', 'management', 'datas', 'flights.json'
        )

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"HATA: JSON dosyası bulunamadı! Yol: {file_path}"))
            return

        self.stdout.write(f"Dosya okundu: {file_path}")

        # Dosyayı baştan okuyalım
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        try:
            # TRANSACTION BAŞLANGICI: Hata olursa buradaki her şey geri alınır
            with transaction.atomic():
                self.stdout.write(self.style.WARNING("\n⚠️  Mevcut veriler temizleniyor..."))

                # 1. ADIM: SİLME İŞLEMİ (Sıralama Önemli!)

                # Önce Flight silinmeli (Çünkü Airport ve Vehicle'a Foreign Key ile bağlı)
                count_flight, _ = Flight.objects.all().delete()
                self.stdout.write(f" - {count_flight} adet Uçuş silindi.")

                # Şimdi bağlı kayıt kalmadığı için diğerlerini silebiliriz
                count_vehicle, _ = VehicleType.objects.all().delete()
                self.stdout.write(f" - {count_vehicle} adet Araç Tipi silindi.")

                count_airport, _ = Airport.objects.all().delete()
                self.stdout.write(f" - {count_airport} adet Havaalanı silindi.")

                self.stdout.write(self.style.SUCCESS("✅ Temizlik tamamlandı. Yükleme başlıyor...\n"))

                # 2. ADIM: YÜKLEME İŞLEMİ

                # --- Havaalanları ---
                self.stdout.write("--- Havaalanları Yükleniyor ---")
                for item in data.get('airports', []):
                    Airport.objects.create(  # Artık get_or_create gerek yok, tablo boş
                        code=item['code'],
                        name=item['name'],
                        city=item['city'],
                        country=item['country']
                    )
                self.stdout.write(self.style.SUCCESS(f"Havaalanları yüklendi."))

                # --- Araç Tipleri ---
                self.stdout.write("--- Araç Tipleri Yükleniyor ---")
                for item in data.get('vehicles', []):
                    VehicleType.objects.create(
                        name=item['name'],
                        seat_count=item['seat_count'],
                        max_crew=item['max_crew'],
                        max_passengers=item['max_passengers']
                    )
                self.stdout.write(self.style.SUCCESS(f"Araçlar yüklendi."))

                # --- Uçuşlar ---
                self.stdout.write("--- Uçuşlar Yükleniyor ---")
                for item in data.get('flights', []):
                    try:
                        source = Airport.objects.get(code=item['source_code'])
                        dest = Airport.objects.get(code=item['destination_code'])
                        vehicle = VehicleType.objects.get(name=item['vehicle_name'])

                        Flight.objects.create(
                            flight_number=item['flight_number'],
                            source=source,
                            destination=dest,
                            vehicle=vehicle,
                            departure_datetime=parse_datetime(item['departure_datetime']),
                            duration_minutes=item['duration_minutes'],
                            distance_km=item['distance_km'],
                            notes=item.get('notes', '')
                        )
                        self.stdout.write(f" + {item['flight_number']} oluşturuldu.")

                    except Exception as e:
                        # Bir uçuşta hata olsa bile transaction sayesinde hepsi iptal olur,
                        # böylece yarım yamalak veri oluşmaz.
                        raise e

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ BİR HATA OLUŞTU! HİÇBİR DEĞİŞİKLİK YAPILMADI.\nHata Detayı: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n🚀 İşlem Başarıyla Tamamlandı! Veritabanı yenilendi."))