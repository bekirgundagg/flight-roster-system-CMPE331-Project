from django.contrib import admin
from .models import Airport, VehicleType, Flight, SharedFlightInfo 
from django.utils.html import format_html

# --- Yeni Modeller İçin Admin Ayarları ---

# 2. SharedFlightInfo (Paylaşımlı Uçuş Bilgisi)
@admin.register(SharedFlightInfo)
class SharedFlightInfoAdmin(admin.ModelAdmin):
    # Ana uçuş numarasını, partneri ve partner uçuş numarasını göster
    list_display = ('get_flight_number', 'partner_airline', 'partner_flight_number', 'connecting_flight')
    search_fields = (
        'flight__flight_number', 
        'partner_airline', 
        'partner_flight_number'
    )
    list_filter = ()

    # Flight modelindeki flight_number'ı liste görünümünde göstermek için metod
    @admin.display(description='Ana Uçuş No')
    def get_flight_number(self, obj):
        return obj.flight.flight_number

# --- Mevcut Modellerin Güncellenmiş Admin Ayarları ---

# Airport modelini Admin'e kaydetme
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    # Modeldeki isim değişikliğini yansıttık (name)
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')
    list_filter = ('country',) 

# VehicleType modelini Admin'e kaydetme
@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    # Modeldeki isim değişikliğini yansıttık (name)
    list_display = ('name', 'seat_count', 'max_crew', 'max_passengers')
    search_fields = ('name',)
    
    # JSONField alanlarının Admin panelinde daha okunaklı görünmesi için
    readonly_fields = ('seating_plan', 'standard_menu') 


# Flight modelini Admin'e kaydetme
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    # Alan isimlerini modelinize göre güncelledik (source, destination, vehicle)
    list_display = (
        'flight_number', 
        'departure_datetime', 
        'source', # source_airport yerine source
        'destination', # destination_airport yerine destination
        'vehicle', # vehicle_type yerine vehicle
        'has_shared_info' # Paylaşımlı uçuş bilgisinin varlığını kontrol eden özel bir alan
    )
    
    # Filtreleme çubuğu
    list_filter = ('departure_datetime', 'vehicle')
    
    # Arama alanları
    search_fields = (
        'flight_number', 
        'source__code', 
        'destination__code'
    )
    
    # Detay sayfasında alanları gruplandırma
    fieldsets = (
        ('Temel Uçuş Bilgileri', {
            'fields': (
                'flight_number', 
                ('departure_datetime', 'duration_minutes', 'distance_km'),
                'notes'
            )
        }),
        ('Kalkış ve Varış', {
            'fields': (
                'source', 
                'destination'
            )
        }),
        ('Uçak Bilgileri', {
            'fields': (
                'vehicle', 
            )
        }),
        # SharedFlightInfo OneToOne olduğu için bu bilgiyi ayrı bir Inlines ile de gösterebiliriz,
        # ama bu fieldsets yapısı şimdilik daha düzenli.
    )

    # Uçuşun Paylaşımlı Bilgisi var mı? (SharedFlightInfo'yu kontrol eder)
    @admin.display(description='Paylaşımlı Uçuş?')
    def has_shared_info(self, obj):
        if hasattr(obj, 'shared_info'):
            return format_html('<span style="color: green; font-weight: bold;">Evet</span>')
        return format_html('<span style="color: red;">Hayır</span>')

    has_shared_info.boolean = False # Sadece görsel bir onay için
