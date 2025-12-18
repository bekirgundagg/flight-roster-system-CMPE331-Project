from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, AirportViewSet, VehicleTypeViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet) 
router.register(r'airports', AirportViewSet) 
router.register(r'vehicle-types', VehicleTypeViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]