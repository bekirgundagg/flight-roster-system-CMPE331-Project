from django.contrib import admin
from .models import Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'flight_id', 'seat_type', 'seat_number', 'age', 'is_infant_status')

    list_filter = ('seat_type', 'gender', 'flight_id')

    search_fields = ('first_name', 'last_name', 'flight_id', 'email')

    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': ('first_name', 'last_name', 'email', 'age', 'gender', 'nationality')
        }),
        ('Uçuş Detayları', {
            'fields': ('flight_id', 'seat_type', 'seat_number')
        }),
        ('Bebek Yolcu Durumu', {
            'fields': ('parent',),
            'description': 'A parent must be selected for passengers aged 0-2..'
        }),
    )

    @admin.display(description='Is infant a passenger?', boolean=True)
    def is_infant_status(self, obj):
        return obj.is_infant