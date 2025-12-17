from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# Model ve Serializer'larını import ediyoruz
from .models import Flight, Airport, VehicleType
from .serializers import FlightSerializer, AirportSerializer, VehicleTypeSerializer
from passengers.models import Passenger
from passengers.serializers import PassengerSerializer


# NOT: 'flights_list' fonksiyonunu sildim çünkü React projesinde
# HTML template render etmeye (render request...) ihtiyacımız yok.
# O hata da bu yüzden gidip, kodun temizlenmiş oldu.

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticated]


class FlightViewSet(viewsets.ModelViewSet):
    # --- DÜZELTME 1: select_related ---
    # Hata mesajında Django dedi ki: "Choices are: source, destination, vehicle"
    # Biz de inatlaşmıyoruz, onun dediği isimleri yazıyoruz.
    queryset = Flight.objects.select_related('source', 'destination', 'vehicle').all()

    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    # --- DÜZELTME 2: Filtreleme ---
    # Filtrelerde de modeldeki isimleri kullanmalıyız.
    # source_airport__code -> source__code
    filterset_fields = ('flight_number', 'source__code', 'destination__code', 'departure_datetime')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flight_roster(request, flight_number):
    try:
        # Pilotları ve Kabin Ekibini de (prefetch) ile çekiyoruz
        flight = Flight.objects.prefetch_related('pilots', 'cabin_crew').get(flight_number=flight_number)
    except Flight.DoesNotExist:
        return Response({"error": "Uçuş bulunamadı"}, status=404)

    # 1. Yolcular
    passengers = Passenger.objects.filter(flight_id=flight_number)

    # 2. EKİP LİSTESİ (Tabular View İçin Veri Hazırlığı)
    crew_data = []

    # A) Pilotları ekle
    for pilot in flight.pilots.all():
        crew_data.append({
            "id": pilot.id,
            "name": pilot.name, # Modelde isim alanı 'name' mi?
            "type": "Pilot",
            "role": pilot.seniority_level, # Dokümanda belirtilen seniority level [cite: 52]
            "avatar": "👨‍✈️"
        })

    # B) Kabin Ekibini ekle
    for member in flight.cabin_crew.all():
        crew_data.append({
            "id": member.attendant_id,
            "name": member.name,
            "type": "Cabin Crew",
            "role": member.attendant_type, # Dokümanda belirtilen attendant type [cite: 60]
            "avatar": "💁‍♀️"
        })

    return Response({
        "flight": FlightSerializer(flight).data,
        "passengers": PassengerSerializer(passengers, many=True).data,
        "crew": crew_data
    })