from django.contrib import admin
from .models import Airport, VehicleType, Flight, SharedFlightInfo 
from django.utils.html import format_html

@admin.register(SharedFlightInfo)
class SharedFlightInfoAdmin(admin.ModelAdmin):
    list_display = ('get_flight_number', 'partner_airline', 'partner_flight_number', 'connecting_flight')
    search_fields = (
        'flight__flight_number', 
        'partner_airline', 
        'partner_flight_number'
    )
    list_filter = ()

    @admin.display(description='Ana Uçuş No')
    def get_flight_number(self, obj):
        return obj.flight.flight_number

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')
    list_filter = ('country',) 

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'seat_count', 'max_crew', 'max_passengers')
    search_fields = ('name',)
    
    readonly_fields = ('seating_plan', 'standard_menu') 

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'flight_number', 
        'departure_datetime', 
        'source', 
        'destination', 
        'vehicle', 
        'has_shared_info' 
    )
    
    list_filter = ('departure_datetime', 'vehicle')
    
    search_fields = (
        'flight_number', 
        'source__code', 
        'destination__code'
    )
    
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
    )


    @admin.display(description='Paylaşımlı Uçuş?')
    def has_shared_info(self, obj):
        if hasattr(obj, 'shared_info'):
            return format_html('<span style="color: green; font-weight: bold;">Evet</span>')
        return format_html('<span style="color: red;">Hayır</span>')

    has_shared_info.boolean = False 
