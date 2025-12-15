from django.test import TestCase
from cabincrew_api.models import CabinCrew, Language


class TestCabinCrewModel(TestCase):

    def setUp(self):
        self.lang = Language.objects.create(lan_name="English")

    def test_crew_creation(self):
        crew = CabinCrew.objects.create(
            attendant_id="CC001",
            name="Ahmet",
            age=30,
            gender="Male",
            nationality="TR",
            attendant_type="regular",
            senority_level="junior",
        )

        crew.known_languages.add(self.lang)

        self.assertEqual(crew.name, "Ahmet")
        self.assertEqual(crew.known_languages.first().lan_name, "English")

    def test_crew_str(self):
        crew = CabinCrew.objects.create(
            attendant_id="CC002",
            name="Ayşe",
            age=28,
            gender="Female",
            nationality="TR",
            attendant_type="chief",
            senority_level="senior",
        )

        self.assertIn("Ayşe", str(crew))

class TestLanguageModel(TestCase):
    def test_language_creation(self):
        lang = Language.objects.create(lan_name="German")
        self.assertEqual(lang.lan_name, "German")

    def test_language_str(self):
        lang = Language.objects.create(lan_name="French")
        self.assertEqual(str(lang), "French")

    def test_cabincrew_multiple_languages(self):
        eng = Language.objects.create(lan_name="English")
        fr = Language.objects.create(lan_name="French")

        crew = CabinCrew.objects.create(
            attendant_id="CC003",
            name="Mehmet",
            age=35,
            gender="Male",
            nationality="TR",
            attendant_type="regular",
            senority_level="senior",
        )

        crew.known_languages.add(eng, fr)

        self.assertEqual(crew.known_languages.count(), 2)




