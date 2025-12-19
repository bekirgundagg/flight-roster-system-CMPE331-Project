from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'TÜM sistemi sıfırlar ve Flights, Pilots, Crew, Passengers verilerini sırasıyla yükler.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("⚠️  BÜTÜN SİSTEM VERİLERİ YENİLENİYOR..."))

        try:
            # 1. ADIM: UÇUŞLAR (Flights, Airports, VehicleTypes)
            self.stdout.write(self.style.MIGRATE_HEADING("\n[1/4] Uçuş Sistemi Yükleniyor..."))
            call_command('load_flights')

            # 2. ADIM: PİLOTLAR (Flight Crew)
            self.stdout.write(self.style.MIGRATE_HEADING("\n[2/4] Pilotlar Yükleniyor..."))
            call_command('load_pilots')

            # 3. ADIM: KABİN EKİBİ (Cabin Crew)
            self.stdout.write(self.style.MIGRATE_HEADING("\n[3/4] Kabin Ekibi Yükleniyor..."))
            call_command('load_cabincrew')

            # 4. ADIM: YOLCULAR (Passengers)
            self.stdout.write(self.style.MIGRATE_HEADING("\n[4/4] Yolcular Yükleniyor..."))
            call_command('load_passengers')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ GENEL BİR HATA OLDU: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n🎉 TEBRİKLER! TÜM SİSTEM BAŞARIYLA KURULDU."))