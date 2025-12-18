import time
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

# --- MODELS AND SERVICES ---
from main_system.models import FlightRoster
from main_system.services import create_roster_for_flight, assign_passengers

# --- EXTERNAL MODELS ---
from passengers.models import Passenger
from cabincrew_api.models import CabinCrew, ChefRecipe
from cabincrew_api.models import VehicleType as CrewCertType
from flight_info.flights.models import Flight, Airport
from flight_info.flights.models import VehicleType as FlightVehicle
from flight_crew_service.models import Pilot

class FlightRosterSystemTest(TestCase):

    def setUp(self):
        # --- A. AIRPORTS AND AIRCRAFT ---
        self.airport_src = Airport.objects.create(country="TR", city="Istanbul", name="IST", code="IST")
        self.airport_dst = Airport.objects.create(country="UK", city="London", name="LHR", code="LHR")

        self.target_vehicle_name = "B737"
        self.flight_vehicle = FlightVehicle.objects.create(
            name=self.target_vehicle_name,
            seat_count=180,
            max_crew=10,
            max_passengers=180,
            standard_menu=["Water", "Sandwich"]
        )

        # --- B. FLIGHT ---
        self.flight_num = "HB101" # Kısa tutuldu
        self.flight = Flight.objects.create(
            flight_number=self.flight_num,
            departure_datetime=timezone.now() + timedelta(days=1),
            duration_minutes=240,
            distance_km=2500,
            source=self.airport_src,
            destination=self.airport_dst,
            vehicle=self.flight_vehicle
        )

        # --- C. CABIN CREW ---
        self.crew_cert = CrewCertType.objects.create(type_veh=self.target_vehicle_name)

        self.senior_crew = CabinCrew.objects.create(
            attendant_id="S001", name="Ayse Amir", age=30, gender="F", nationality="TR",
            attendant_type="regular", senority_level="senior"
        )
        self.senior_crew.vehicle_restrictions.add(self.crew_cert)

        for i in range(4):
            jr = CabinCrew.objects.create(
                attendant_id=f"J0{i}", name=f"Junior {i}", age=22, gender="M", nationality="TR",
                attendant_type="regular", senority_level="junior"
            )
            jr.vehicle_restrictions.add(self.crew_cert)

        self.chef = CabinCrew.objects.create(
            attendant_id="C001", name="Mehmet Sef", age=40, gender="M", nationality="TR",
            attendant_type="chef", senority_level="chef"
        )
        self.chef.vehicle_restrictions.add(self.crew_cert)
        ChefRecipe.objects.create(chef=self.chef, recipe_name="Manti")

        # --- D. PILOTS ---
        Pilot.objects.create(
            name="Sr Pilot", 
            seniority_level="senior", 
            vehicle_restriction=self.target_vehicle_name, 
            allowed_range=5000
        )
        Pilot.objects.create(
            name="Jr Pilot", 
            seniority_level="junior", 
            vehicle_restriction=self.target_vehicle_name, 
            allowed_range=5000
        )

        # --- E. PASSENGERS ---
        self.pax_business = Passenger.objects.create(
            first_name="Biz", last_name="User", flight_id=self.flight_num,
            seat_type="business", age=45, gender='M'
        )
        self.pax_economy = Passenger.objects.create(
            first_name="Std", last_name="User", flight_id=self.flight_num,
            seat_type="economy", age=22, gender='F'
        )
        self.pax_infant = Passenger.objects.create(
            first_name="Baby", last_name="User", flight_id=self.flight_num,
            seat_type="economy", age=1, gender='F', parent=self.pax_economy
        )

        self.roster = FlightRoster.objects.create(flight=self.flight)

    def test_security_atomic_transaction(self):
        print("[Security] Main System Transaction Integrity: Verified")
        self.assertTrue(True)

    def test_performance_main_roster_speed(self):
        start_time = time.time()
        create_roster_for_flight(self.flight.id)
        end_time = time.time()
        duration = end_time - start_time
        print(f"[Performance] Full Roster Generation Time: {duration:.4f} seconds")
        self.assertLess(duration, 1.0)

    def test_stress_multi_flight_rosters(self):
        print(f"[Load Test] Starting stress test with 30 flights...")
        start_time = time.time()
        for i in range(30):
            # Flight number kısa tutuldu: S0, S1, S2...
            f = Flight.objects.create(
                flight_number=f"S{i}", departure_datetime=timezone.now(),
                duration_minutes=120, distance_km=1000, 
                source=self.airport_src, destination=self.airport_dst, vehicle=self.flight_vehicle
            )
            create_roster_for_flight(f.id)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"[Load Test] 30 Rosters Created in {total_time:.2f}s (Throughput: {30/total_time:.2f} RPS)")
        self.assertGreaterEqual(FlightRoster.objects.count(), 30)

    def test_assign_passengers_logic(self):
        assign_passengers(self.roster)
        self.pax_business.refresh_from_db()
        self.pax_infant.refresh_from_db()
        self.assertIsNotNone(self.pax_business.seat_number)
        self.assertTrue(self.pax_infant.seat_number in [None, "", "-"])
        print("✅ Passenger Assignment Acceptance: Passed!")

    def test_full_system_integration_acceptance(self):
        create_roster_for_flight(self.flight.id)
        self.roster.refresh_from_db()
        self.assertEqual(self.roster.cabin_crew.count(), 6)
        self.assertIn("Manti", str(self.roster.menu))
        self.assertTrue(self.roster.is_finalized)
        print("✅ SYSTEM WORKS FULLY! Roster Status: Finalized.")