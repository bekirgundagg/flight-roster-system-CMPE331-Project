from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import MagicMock, patch

# --- SERVICES AND MODELS ---
from main_system.models import FlightRoster
from main_system.services import create_roster_for_flight, assign_passengers

# --- 1. PASSENGER MODEL ---
from passengers.models import Passenger

# --- 2. CABIN CREW MODELS ---
from cabincrew_api.models import CabinCrew, ChefRecipe
from cabincrew_api.models import VehicleType as CrewCertType

# --- 3. FLIGHT INFO MODELS ---
from flight_info.flights.models import Flight, Airport
from flight_info.flights.models import VehicleType as FlightVehicle

# --- 4. PILOT MODEL (To be mocked) ---
from flight_crew_service.models import Pilot


class FlightRosterSystemTest(TestCase):

    def setUp(self):
        """
        Setup: Initialize the full scenario with real database records.
        """
        # --- A. AIRPORTS AND AIRCRAFT ---
        self.airport_src = Airport.objects.create(country="TR", city="Istanbul", name="IST", code="IST")
        self.airport_dst = Airport.objects.create(country="UK", city="London", name="LHR", code="LHR")

        # Aircraft Type: B737 (180 Seats)
        self.target_vehicle_name = "B737"
        self.flight_vehicle = FlightVehicle.objects.create(
            name=self.target_vehicle_name,
            seat_count=180,
            max_crew=10,
            max_passengers=180,
            standard_menu=["Water", "Sandwich"]
        )

        # --- B. FLIGHT ---
        self.flight_num = "HB1001"
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

        # Create 1 Senior + 4 Juniors + 1 Chef = 6 Crew Members
        self.senior_crew = CabinCrew.objects.create(
            attendant_id="S001", name="Ayşe Amir", age=30, gender="F", nationality="TR",
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
            attendant_id="C001", name="Mehmet Şef", age=40, gender="M", nationality="TR",
            attendant_type="chef", senority_level="chef"
        )
        self.chef.vehicle_restrictions.add(self.crew_cert)
        ChefRecipe.objects.create(chef=self.chef, recipe_name="Mantı")

        # --- D. PASSENGERS ---
        # Passenger model uses flight_id as String ('HB1001')

        # 1. Business Passenger (No seat initially)
        self.pax_business = Passenger.objects.create(
            first_name="Business", last_name="User",
            flight_id=self.flight_num,
            seat_type="business",
            age=45, gender='M'
        )

        # 2. Economy Passenger (No seat initially)
        self.pax_economy = Passenger.objects.create(
            first_name="Student", last_name="User",
            flight_id=self.flight_num,
            seat_type="economy",
            age=22, gender='F'
        )

        # 3. Infant Passenger (0-2 Years -> Should NOT get a seat)
        self.pax_infant = Passenger.objects.create(
            first_name="Baby", last_name="User",
            flight_id=self.flight_num,
            seat_type="economy",
            age=1,
            gender='F',
            parent=self.pax_economy  # Traveling with parent
        )

        # Initialize Roster
        self.roster = FlightRoster.objects.create(flight=self.flight)

    def test_assign_passengers_logic(self):
        """
        Tests only the passenger assignment logic.
        """
        # Execute function
        assign_passengers(self.roster)

        # Refresh data from DB
        self.pax_business.refresh_from_db()
        self.pax_economy.refresh_from_db()
        self.pax_infant.refresh_from_db()

        # 1. Check Business Passenger
        print(f"Business Seat: {self.pax_business.seat_number}")
        self.assertIsNotNone(self.pax_business.seat_number)
        self.assertTrue(len(self.pax_business.seat_number) >= 2)

        # 2. Check Economy Passenger
        print(f"Economy Seat: {self.pax_economy.seat_number}")
        self.assertIsNotNone(self.pax_economy.seat_number)

        # 3. Check Infant Passenger (CRITICAL)
        # Infants should not be assigned a seat!
        print(f"Infant Seat: {self.pax_infant.seat_number}")
        self.assertTrue(
            self.pax_infant.seat_number in [None, "", "-"],
            "Infant passenger should not have an assigned seat!"
        )

        # 4. Verify Roster inclusion
        self.assertEqual(self.roster.passengers.count(), 3, "All passengers (including infant) must be added to the list")

        print("✅ Passenger Assignment Test Passed!")

    @patch('main_system.services.assign_pilots')
    def test_full_roster_creation_process(self, mock_assign_pilots_func):
        """
        End-to-End Test (Create Roster For Flight).
        Mocks pilot assignment to focus on system integration stability.
        """
        # 1. Mock assign_pilots to return True (simulate success)
        mock_assign_pilots_func.return_value = True

        # --- EXECUTE MAIN FUNCTION ---
        create_roster_for_flight(self.flight.id)

        # -----------------------------------------------------------
        # Refresh the roster instance from DB to get updated fields
        # (menu, finalized status, relations)
        self.roster.refresh_from_db()
        # -----------------------------------------------------------

        # --- ASSERTIONS ---

        # 1. Was assign_pilots called?
        args, _ = mock_assign_pilots_func.call_args
        self.assertEqual(args[0].flight.id, self.flight.id)

        # 2. Verify Cabin Crew assignment
        self.assertEqual(self.roster.cabin_crew.count(), 6)

        # 3. Verify Menu generation (Should include Chef's Special)
        print(f"DEBUG MENU: {self.roster.menu}")
        self.assertIn("Mantı", str(self.roster.menu))

        # 4. Verify Passengers assignment
        self.assertEqual(self.roster.passengers.count(), 3)

        # 5. Is Roster finalized?
        self.assertTrue(self.roster.is_finalized)

        print(f"✅ SYSTEM WORKS FULLY! Roster Status: Finalized.")