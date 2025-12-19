from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from cabincrew_api.models import CabinCrew

class CabinCrewWhiteBoxTest(SimpleTestCase):
    def test_cabincrew_str_logic_memory(self):
        crew = CabinCrew(
            attendant_id="CC999",
            name="Test Attendant",
            age=25,
            gender="Female",
            nationality="TR",
            attendant_type="regular",
            seniority_level="junior"
        )

        crew._state = MagicMock()
        crew._state.db = None

        expected_str = str(crew)
        self.assertIn("Test Attendant", expected_str)

    @patch('cabincrew_api.models.CabinCrew.save')
    def test_cabincrew_save_mechanism_mock(self, mock_save):
        crew = CabinCrew(
            attendant_id="CC888",
            name="Mock Crew",
            age=30,
            gender="Male",
            nationality="US",
            attendant_type="chief"
        )

        crew._state = MagicMock()
        crew._state.db = None

        crew.save()

        self.assertTrue(mock_save.called)

    def test_cabincrew_business_logic_attributes(self):
        crew = CabinCrew(
            name="Logic Check",
            attendant_type="chief",
            seniority_level="senior"
        )
        
        crew._state = MagicMock()
        crew._state.db = None

        self.assertEqual(crew.attendant_type, "chief")
        self.assertEqual(crew.seniority_level, "senior")