import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
# Flight Crew Service modellerini import ediyoruz
from flight_crew_service.models import Pilot, Language


class Command(BaseCommand):
    help = 'Mevcut Pilot ve Dil verilerini TEMİZLER ve JSON dosyasından yeniden yükler'

    def handle(self, *args, **kwargs):
        # Dosya yolunu belirle (Aynı klasör yapısı)
        file_path = os.path.join(
            settings.BASE_DIR,
            'main_system', 'management', 'datas', 'pilots.json'
        )

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"HATA: JSON dosyası bulunamadı! Yol: {file_path}"))
            return

        self.stdout.write(f"Dosya okundu: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        try:
            # GÜVENLİK: Hata olursa her şeyi geri al (Rollback)
            with transaction.atomic():
                self.stdout.write(self.style.WARNING("\n⚠️  Mevcut Pilot ve Dil verileri temizleniyor..."))

                # 1. ADIM: SİLME (Önce Pilotlar silinmeli çünkü Diller onlara bağlı)
                count_pilot, _ = Pilot.objects.all().delete()
                self.stdout.write(f" - {count_pilot} adet Pilot silindi.")

                count_lang, _ = Language.objects.all().delete()
                self.stdout.write(f" - {count_lang} adet Dil silindi.")

                self.stdout.write(self.style.SUCCESS("✅ Temizlik tamamlandı. Yükleme başlıyor...\n"))

                # 2. ADIM: YÜKLEME

                # --- A) Dilleri Yükle ---
                self.stdout.write("--- Diller Yükleniyor ---")
                # JSON'daki diller listesini dönüyoruz
                for lang_name in data.get('languages', []):
                    Language.objects.create(language_name=lang_name)
                self.stdout.write(self.style.SUCCESS("Diller veritabanına işlendi."))

                # --- B) Pilotları Yükle ---
                self.stdout.write("--- Pilotlar Yükleniyor ---")
                for item in data.get('pilots', []):
                    # Önce Pilot objesini oluşturuyoruz
                    pilot = Pilot.objects.create(
                        name=item['name'],
                        age=item.get('age'),  # get ile alıyoruz, yoksa None olur (blank=True)
                        gender=item.get('gender'),
                        nationality=item.get('nationality'),
                        seniority_level=item['seniority_level'],
                        allowed_range=item['allowed_range'],
                        vehicle_restriction=item['vehicle_restriction']
                    )

                    # --- Many-to-Many İlişkisi (Diller) ---
                    # JSON'daki 'known_languages' listesindeki her dil ismini
                    # Veritabanındaki Language objesiyle eşleştirip pilota ekliyoruz.
                    languages_to_add = item.get('known_languages', [])
                    for lang_str in languages_to_add:
                        try:
                            lang_obj = Language.objects.get(language_name=lang_str)
                            pilot.languages.add(lang_obj)  # İlişkiyi kuruyoruz
                        except Language.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(f"UYARI: '{lang_str}' dili sistemde tanımlı değil, atlanıyor."))

                    self.stdout.write(f" + {pilot.name} ({pilot.seniority_level}) oluşturuldu.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ BİR HATA OLUŞTU! HİÇBİR DEĞİŞİKLİK YAPILMADI.\nHata Detayı: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n🚀 İşlem Başarıyla Tamamlandı! Pilot veritabanı yenilendi."))