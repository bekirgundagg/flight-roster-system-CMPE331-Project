from rest_framework import serializers
from .models import Airport, VehicleType, Flight

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'code', 'country', 'city', 'name']

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    source_detail = AirportSerializer(source='source', read_only=True)
    destination_detail = AirportSerializer(source='destination', read_only=True)
    vehicle_detail = VehicleTypeSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 
            'flight_number', 
            'departure_datetime', 
            'duration_minutes', 
            'distance_km',
            'source',        
            'destination',  
            'vehicle',     
            'notes',
            'source_detail', 
            'destination_detail', 
            'vehicle_detail'
        ]