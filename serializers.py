from rest_framework import serializers
from .models import Airport, VehicleType, Flight

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['code', 'country', 'city', 'name']

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__' # Tüm alanları dahil et

class FlightSerializer(serializers.ModelSerializer):
    # Havaalanı bilgilerini kod yerine detaylı göstermek için
    source_airport = AirportSerializer(read_only=True)
    destination_airport = AirportSerializer(read_only=True)
    vehicle_type = VehicleTypeSerializer(read_only=True)
    
    # Sadece kodları alıp modelde Foreign Key'i doğru kurmak için
    source_airport_code = serializers.CharField(write_only=True)
    destination_airport_code = serializers.CharField(write_only=True)
    vehicle_type_model = serializers.CharField(write_only=True)


    class Meta:
        model = Flight
        fields = [
            'flight_number', 'departure_datetime', 'duration_minutes', 'distance_km',
            'source_airport', 'destination_airport', 'vehicle_type', 
            'is_shared', 'shared_company_name', 'shared_flight_number', 'connecting_flight_info',
            'source_airport_code', 'destination_airport_code', 'vehicle_type_model' # write_only alanlar
        ]
        read_only_fields = ('source_airport', 'destination_airport', 'vehicle_type')

    # Bu metod, oluşturma/güncelleme sırasında FK alanlarını doğru nesnelere dönüştürmek için önemlidir
    def create(self, validated_data):
        # write_only alanları veriden çıkarıp FK nesnelerine dönüştürme
        source_code = validated_data.pop('source_airport_code')
        destination_code = validated_data.pop('destination_airport_code')
        vehicle_model = validated_data.pop('vehicle_type_model')

        validated_data['source_airport'] = Airport.objects.get(code=source_code)
        validated_data['destination_airport'] = Airport.objects.get(code=destination_code)
        validated_data['vehicle_type'] = VehicleType.objects.get(model_name=vehicle_model)
        
        return Flight.objects.create(**validated_data)
        
    # Güncelleme için de benzer mantık uygulanabilir
    # def update(self, instance, validated_data):
    #     ...