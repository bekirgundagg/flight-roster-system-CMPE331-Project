from django.db import models

# Diğer App'lerden modelleri çekiyoruz (Entegrasyon burada başlıyor)
from flight_info.flights.models import Flight
from flight_crew_service.models import Pilot
from cabincrew_api.models import CabinCrew
from passengers.models import Passenger


class FlightRoster(models.Model):
    # Her roster bir uçuşa aittir
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE, related_name='roster')

    # Roster oluşturulurken seçilen ekip
    pilots = models.ManyToManyField(Pilot, related_name='rosters')
    cabin_crew = models.ManyToManyField(CabinCrew, related_name='rosters')
    menu = models.JSONField(null=True, blank=True, verbose_name="Uçuş Menüsü")
    # O uçuşa atanan yolcular
    passengers = models.ManyToManyField(Passenger, related_name='rosters', blank=True)
    is_finalized = models.BooleanField(default=False, verbose_name="Roster Onaylandı mı?")
    # Roster statüsü
    is_generated = models.BooleanField(default=False, help_text="Otomatik oluşturma tamamlandı mı?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roster: {self.flight.flight_number}"