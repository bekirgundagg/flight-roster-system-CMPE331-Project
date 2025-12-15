from django.shortcuts import render

from rest_framework import viewsets
from .models import Flight, Airport, VehicleType 
from .serializers import FlightSerializer, AirportSerializer, VehicleTypeSerializer
from rest_framework.permissions import IsAuthenticated # Veya belirlediğiniz Authorization/Authentication

def flights_list(request):
    airline = airline.objects.first()  # tek havayolu
    flights = Flight.objects.filter(airline=airline).order_by('departure_datetime')
    return render(request, "flights_list.html", {"flights": flights})
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated] # Yetkilendirmeyi daha sonra ayarlayabilirsiniz

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticated]

class FlightViewSet(viewsets.ModelViewSet):
    # Ana sistemin uçuşları filtrelemesi için bir sorgu seti.
    # Uçuş numarasına göre veya diğer alanlara göre filtreleme sağlar
    queryset = Flight.objects.select_related('source_airport', 'destination_airport', 'vehicle_type').all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    # Uçuş numarası (flight_number) ile arama yapmayı etkinleştirin
    filter_fields = ('flight_number', 'source_airport__code', 'destination_airport__code', 'departure_datetime') 
    # Bu özellik için 'django-filter' paketini kurmanız gerekebilir: pip install django-filter
