from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, AirportViewSet, VehicleTypeViewSet, get_flight_roster, auto_assign_crew

# Router oluşturma ve ViewSet'leri kaydetme
router = DefaultRouter()
router.register(r'flights', FlightViewSet) # /api/v1/flights/
router.register(r'airports', AirportViewSet) # /api/v1/airports/
router.register(r'vehicle-types', VehicleTypeViewSet) # /api/v1/vehicle-types/

urlpatterns = [
    path('', include(router.urls)),
    path('roster/<str:flight_number>/', get_flight_roster, name='flight-roster'),
    path('roster/<str:flight_number>/auto-assign/', auto_assign_crew, name='auto-assign-crew'),
]