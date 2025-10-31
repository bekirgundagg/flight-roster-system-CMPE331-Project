from django.shortcuts import render

from rest_framework import viewsets

from .models import CabinCrew, VehicleType, ChefRecipe  
from .serializers import CabinCrewSerializer, VehicleTypeSerializer, ChefRecipeSerializer

class CabinCrewViewSet(viewsets.ModelViewSet):
    
    queryset = CabinCrew.objects.all()
    serializer_class = CabinCrewSerializer

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

class ChefRecipeViewSet(viewsets.ModelViewSet): 
    queryset = ChefRecipe.objects.all()
    serializer_class = ChefRecipeSerializer

