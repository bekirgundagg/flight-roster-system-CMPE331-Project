from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Flight, Airport, VehicleType
from .serializers import FlightSerializer, AirportSerializer, VehicleTypeSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticated]

class FlightViewSet(viewsets.ModelViewSet):
    """
    Uçuşları listeler, oluşturur ve yönetir.
    Testlerin geçtiği ve modellerle uyumlu olan versiyon budur.
    """
    queryset = Flight.objects.select_related('source', 'destination', 'vehicle').all()
    
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = ('flight_number', 'source__code', 'destination__code', 'departure_datetime')