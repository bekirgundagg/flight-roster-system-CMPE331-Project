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

    source_airport = AirportSerializer(source='source', read_only=True)
    destination_airport = AirportSerializer(source='destination', read_only=True)
    vehicle_type = VehicleTypeSerializer(source='vehicle', read_only=True)

    source_airport_code = serializers.CharField(write_only=True)
    destination_airport_code = serializers.CharField(write_only=True)
    vehicle_type_model = serializers.CharField(write_only=True)

    class Meta:
        model = Flight
        fields = [
            'flight_number', 'departure_datetime', 'duration_minutes', 'distance_km',
            'source_airport', 'destination_airport', 'vehicle_type',
            'source_airport_code', 'destination_airport_code', 'vehicle_type_model'
        ]
        read_only_fields = ('source_airport', 'destination_airport', 'vehicle_type')

    def create(self, validated_data):
        source_code = validated_data.pop('source_airport_code')
        destination_code = validated_data.pop('destination_airport_code')
        vehicle_model = validated_data.pop('vehicle_type_model')

        # Model alan isimlerine göre atamalar
        validated_data['source'] = Airport.objects.get(code=source_code)
        validated_data['destination'] = Airport.objects.get(code=destination_code)
        validated_data['vehicle'] = VehicleType.objects.get(model_name=vehicle_model)

        return Flight.objects.create(**validated_data)