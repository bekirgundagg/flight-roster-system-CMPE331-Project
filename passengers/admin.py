from django.contrib import admin
from .models import Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    # Liste görünümünde hangi sütunlar olsun?
    list_display = ('first_name', 'last_name', 'flight_id', 'seat_type', 'seat_number', 'age', 'is_infant_status')

    # Yan panelde filtreleme seçenekleri
    list_filter = ('seat_type', 'gender', 'flight_id')

    # Arama çubuğu hangi alanlarda arasın?
    search_fields = ('first_name', 'last_name', 'flight_id', 'email')

    # Düzenleme ekranında alanları gruplayalım
    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': ('first_name', 'last_name', 'email', 'age', 'gender', 'nationality')
        }),
        ('Uçuş Detayları', {
            'fields': ('flight_id', 'seat_type', 'seat_number')
        }),
        ('Bebek Yolcu Durumu', {
            'fields': ('parent',),
            'description': '0-2 yaş arasındaki yolcular için ebeveyn seçilmelidir.'
        }),
    )

    # Admin panelinde True/False yerine ikonla göstermek için özel metod
    @admin.display(description='Bebek Yolcu mu?', boolean=True)
    def is_infant_status(self, obj):
        return obj.is_infant