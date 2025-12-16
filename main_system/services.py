import random
import math
from django.db import transaction

from .models import FlightRoster
from flight_info.flights.models import Flight
from flight_crew_service.models import Pilot
from cabincrew_api.models import CabinCrew
from passengers.models import Passenger


def assign_pilots(roster):
    """
    Yardımcı Fonksiyon: Pilot atama mantığı.
    """
    flight = roster.flight
    vehicle_name = flight.vehicle.name
    distance = flight.distance_km

    # ADIM 1: Uygun Adayları Bul (Filtreleme)
    # Kural: Pilotun araç tipi uçağa uymalı VE menzili yetmeli
    candidates = Pilot.objects.filter(
        vehicle_restriction=vehicle_name,
        allowed_range__gte=distance
    )

    if not candidates.exists():
        print(f"HATA: {vehicle_name} için {distance}km menzilli pilot bulunamadı!")
        return False

    # ADIM 2: Kıdemlerine Göre Grupla
    seniors = list(candidates.filter(senority_level='senior'))
    juniors = list(candidates.filter(senority_level='junior'))
    trainees = list(candidates.filter(senority_level='trainee'))

    # ADIM 3: Yeterlilik Kontrolü (1 Senior + 1 Junior Şartı)
    if not seniors:
        print("HATA: Uygun Senior pilot yok.")
        return False
    if not juniors:
        print("HATA: Uygun Junior pilot yok.")
        return False

    # Greedy yaklaşımıyla rastgele seçim
    selected_senior = random.choice(seniors)
    selected_junior = random.choice(juniors)

    roster.pilots.add(selected_senior)
    roster.pilots.add(selected_junior)

    # Opsiyonel: Büyük uçaklar için trainee eklenebilir
    if trainees and flight.vehicle.seat_count > 100:
        selected_trainee = random.choice(trainees)
        roster.pilots.add(selected_trainee)

    return True


def assign_cabin_crew(roster):
    """
    Kabin ekibi atama mantığı.
    Kurallar:
    1. Personel o uçak tipinde çalışabilmeli (Vehicle Restriction).
    2. 1-4 arası Senior, 4-16 arası Junior, 0-2 arası Chef seçilmeli.
    3. Seçilen şeflerin tariflerinden biri menüye eklenmeli.
    """
    flight = roster.flight
    vehicle_name = flight.vehicle.name

    # ADAYLARI FİLTRELE
    candidates = CabinCrew.objects.filter(
        vehicle_restrictions__type_veh=vehicle_name,
    ).distinct()

    if not candidates.exists():
        print("HATA: Bu uçak tipi için uygun kabin ekibi bulunamadı!")
        return False

    # GRUPLAMA
    seniors = list(candidates.filter(senority_level='senior'))
    juniors = list(candidates.filter(senority_level='junior'))
    chefs = list(candidates.filter(senority_level='chef'))

    # YETERLİLİK KONTROLÜ (MİNİMUM SAYILAR)
    if len(seniors) < 1:
        print("ERROR: There is no enough senior attendant")
        return False
    if len(juniors) < 4:
        print("ERROR: There is no enough junior attendant")
        return False

    # SEÇİM (RANDOM)
    num_seniors = random.randint(1, min(4, len(seniors)))
    selected_seniors = random.sample(seniors, num_seniors)

    num_juniors = random.randint(4, min(16, len(juniors)))
    selected_juniors = random.sample(juniors, num_juniors)

    num_chefs = random.randint(0, min(2, len(chefs)))
    selected_chefs = random.sample(chefs, num_chefs)

    # ROSTER'A EKLE
    all_crew = selected_seniors + selected_juniors + selected_chefs
    for crew in all_crew:
        roster.cabin_crew.add(crew)

    # MENÜ HAZIRLA
    final_menu = []

    standard = roster.flight.vehicle.standard_menu
    if standard:
        if isinstance(standard, list):
            final_menu.extend(standard)
        else:
            final_menu.append(standard)

    for chef in selected_chefs:
        chef_recipes = list(chef.recipes.all())
        if chef_recipes:
            chosen_recipe = random.choice(chef_recipes)
            final_menu.append({
                "type": "Chef's Special",
                "name": chosen_recipe.recipe_name,
                "chef": getattr(chef, "name", str(chef))
            })
            print(f"Özel Tarif Eklendi: {chosen_recipe.recipe_name}")

    roster.menu = final_menu
    roster.save()

    print(f"Kabin Ekibi ve Menü Hazır. Toplam Personel: {roster.cabin_crew.count()}")
    return True


def generate_seat_map(row_count, start_row=1):
    """
    Yardımcı Fonksiyon: Basit koltuk listesi üretir.
    Örn: ['1A', '1B', '1C', '1D', '1E', '1F', '2A'...]
    """
    seats = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F']  # Tek koridorlu uçak varsayımı
    for row in range(start_row, start_row + row_count):
        for letter in letters:
            seats.append(f"{row}{letter}")
    return seats


def assign_passengers(roster):
    """
    Yolcuları bulur, Roster'a ekler ve koltuğu olmayanlara koltuk atar.
    Kurallar:
    1. Passenger modelindeki 'flight_id' ile Roster'daki uçuş numarası eşleşmeli.
    2. Bebeklere (0-2 yaş) koltuk atanmaz.
    3. Business ve Economy yolcuları kendi bölümlerine oturmalı.
    4. Koltuk numarası olmayanlara, boş olan koltuklardan biri verilmeli.
    """
    flight = roster.flight
    vehicle = flight.vehicle

    print(f"--- Yolcu Atama Başladı: {flight.flight_number} ---")

    # 1) YOLCULARI BUL
    flight_passengers = Passenger.objects.filter(flight_id=flight.flight_number)

    if not flight_passengers.exists():
        print("WARNING: There is no passenger for this flight.")
        return True  # hata değil

    # 2) ROSTER'A SET ET
    roster.passengers.set(flight_passengers)

    # 3) DOLU KOLTUKLARI VE KOLTUKSIZLARI AYIR
    occupied_seats = set()
    passengers_needing_seats = []

    for p in flight_passengers:
        if p.seat_number:
            occupied_seats.add(p.seat_number)
        else:
            passengers_needing_seats.append(p)

    # 4) KOLTUK HAVUZLARINI OLUŞTUR
    # seat_count 6'ya tam bölünmüyorsa ceil kullanmak daha güvenli
    total_rows = max(1, math.ceil(vehicle.seat_count / 6))

    business_rows = min(5, total_rows)          # ilk 5 satır business
    economy_rows = max(0, total_rows - business_rows)

    business_seats_pool = generate_seat_map(row_count=business_rows, start_row=1)
    economy_seats_pool = generate_seat_map(row_count=economy_rows, start_row=business_rows + 1)

    # 5) KULLANIMA HAZIR (BOŞ) KOLTUK LİSTELERİNİ HAZIRLA
    available_business = [s for s in business_seats_pool if s not in occupied_seats]
    available_economy = [s for s in economy_seats_pool if s not in occupied_seats]

    assigned_count = 0

    # 6) KOLTUK ATA
    for p in passengers_needing_seats:
        # Bebeklere koltuk yok
        if p.age is not None and p.age <= 2:
            print(f"Bilgi: Bebek yolcu {p.first_name} için koltuk atanmadı.")
            continue

        seat_type = (p.seat_type or "").lower().strip()
        if seat_type == "business":
            pool = available_business
        else:
            pool = available_economy

        if not pool:
            print(f"HATA: {seat_type or 'economy'} için boş koltuk kalmadı! Yolcu: {p.first_name}")
            continue

        # "Boş koltuklardan biri" -> rastgele atayalım
        selected_seat = random.choice(pool)
        pool.remove(selected_seat)

        p.seat_number = selected_seat
        p.save(update_fields=["seat_number"])

        occupied_seats.add(selected_seat)
        assigned_count += 1

        print(f"Atama: {p.first_name} ({seat_type or 'economy'}) -> {selected_seat}")

    # ✅ EN KRİTİK DÜZELTME: return True artık döngünün DIŞINDA
    print(
        f"Yolcu İşlemleri Bitti. Roster'a {flight_passengers.count()} kişi eklendi. "
        f"{assigned_count} kişiye yeni koltuk atandı."
    )

    return True


@transaction.atomic
def create_roster_for_flight(flight_id):
    """
    Verilen uçuş ID'si için otomatik bir Roster oluşturur.
    """
    # 1) Uçuşu bul
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return "Hata: Böyle bir uçuş bulunamadı."

    # 2) Roster nesnesini oluştur (veya varsa getir)
    roster, created = FlightRoster.objects.get_or_create(flight=flight)

    if not created and roster.is_finalized:
        return "Bu uçuş zaten planlanmış ve onaylanmış!"

    # Eğer daha önce oluşturulmuş ama finalize edilmemişse, tekrar üretirken birikme olmasın
    if not created:
        roster.pilots.clear()
        roster.cabin_crew.clear()
        roster.passengers.clear()
        roster.menu = []
        roster.save()

    # 3) Pilot Ataması
    if not assign_pilots(roster):
        return "Roster oluşturulamadı: Uygun kriterlerde pilot bulunamadı."

    # 4) Kabin Ekibi Ataması
    if not assign_cabin_crew(roster):
        return "Roster oluşturulamadı: Yeterli kabin ekibi yok."

    # 5) Yolcu/Koltuk Ataması
    assign_passengers(roster)

    # 6) Finalize
    roster.is_finalized = True
    roster.save()

    return roster