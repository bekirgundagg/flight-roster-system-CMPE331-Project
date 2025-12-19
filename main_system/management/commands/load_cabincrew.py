import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
# Model importları (senin verdiğin models yapısına göre)
from cabincrew_api.models import CabinCrew, Language, VehicleType, ChefRecipe


class Command(BaseCommand):
    help = 'Mevcut Kabin Ekibi verilerini TEMİZLER ve JSON dosyasından yeniden yükler'

    def handle(self, *args, **kwargs):
        # Dosya yolunu belirle
        file_path = os.path.join(
            settings.BASE_DIR,
            'main_system', 'management', 'datas', 'cabincrew.json'
        )

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"HATA: JSON dosyası bulunamadı! Yol: {file_path}"))
            return

        self.stdout.write(f"Dosya okundu: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        try:
            with transaction.atomic():
                self.stdout.write(self.style.WARNING("\n⚠️  Mevcut Kabin Ekibi verileri temizleniyor..."))

                # 1. ADIM: SİLME SIRASI (Çocuktan Babaya)
                # Önce tarifler silinmeli (Crew'a bağlı)
                count_recipes, _ = ChefRecipe.objects.all().delete()

                # Sonra Crew silinmeli (Language ve VehicleType'a bağlı)
                count_crew, _ = CabinCrew.objects.all().delete()

                # En son bağımsız tablolar
                count_lang, _ = Language.objects.all().delete()
                count_vehicle, _ = VehicleType.objects.all().delete()

                self.stdout.write(
                    f" - {count_recipes} Tarif, {count_crew} Personel, {count_lang} Dil ve {count_vehicle} Araç Tipi silindi.")
                self.stdout.write(self.style.SUCCESS("✅ Temizlik tamamlandı. Yükleme başlıyor...\n"))

                # 2. ADIM: YÜKLEME

                # --- A) Dilleri Yükle ---
                self.stdout.write("--- Diller Yükleniyor ---")
                for lan in data.get('languages', []):
                    Language.objects.create(lan_name=lan)
                self.stdout.write(self.style.SUCCESS("Diller işlendi."))

                # --- B) Araç Tiplerini Yükle ---
                self.stdout.write("--- Araç Tipleri Yükleniyor ---")
                for v_type in data.get('vehicle_types', []):
                    VehicleType.objects.create(type_veh=v_type)
                self.stdout.write(self.style.SUCCESS("Araç tipleri işlendi."))

                # --- C) Kabin Ekibini Yükle ---
                self.stdout.write("--- Personel Yükleniyor ---")
                for item in data.get('crew_members', []):

                    # 1. Kabin Memuru Objesini Yarat
                    crew_member = CabinCrew.objects.create(
                        attendant_id=item['id'],
                        name=item['name'],
                        age=item['age'],
                        gender=item['gender'],
                        nationality=item['nationality'],
                        attendant_type=item['attendant_type'],
                        seniority_level=item['seniority_level']
                    )

                    # 2. Dilleri Eşleştir (Many-to-Many)
                    for lan_str in item.get('languages', []):
                        try:
                            l_obj = Language.objects.get(lan_name=lan_str)
                            crew_member.known_languages.add(l_obj)
                        except Language.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Dil bulunamadı: {lan_str}"))

                    # 3. Araç Kısıtlamalarını Eşleştir (Many-to-Many)
                    for veh_str in item.get('allowed_vehicles', []):
                        try:
                            v_obj = VehicleType.objects.get(type_veh=veh_str)
                            crew_member.vehicle_restrictions.add(v_obj)
                        except VehicleType.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Araç tipi bulunamadı: {veh_str}"))

                    # 4. Eğer Aşçıysa Tariflerini Ekle (One-to-Many)
                    recipes = item.get('recipes', [])
                    if recipes:
                        for recipe_name in recipes:
                            ChefRecipe.objects.create(
                                chef=crew_member,
                                recipe_name=recipe_name
                            )
                        self.stdout.write(f" + {crew_member.name} (Şef) ve {len(recipes)} tarifi eklendi.")
                    else:
                        self.stdout.write(f" + {crew_member.name} ({crew_member.attendant_type}) eklendi.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ BİR HATA OLUŞTU! HİÇBİR DEĞİŞİKLİK YAPILMADI.\nHata Detayı: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n🚀 İşlem Başarıyla Tamamlandı! Kabin ekibi veritabanı yenilendi."))