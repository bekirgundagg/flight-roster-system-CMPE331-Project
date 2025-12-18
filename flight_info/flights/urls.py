from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, AirportViewSet, VehicleTypeViewSet, get_flight_roster, auto_assign_crew

router = DefaultRouter()
router.register(r'flights', FlightViewSet) 
router.register(r'airports', AirportViewSet) 
router.register(r'vehicle-types', VehicleTypeViewSet) 

urlpatterns = [
    path('', include(router.urls)),
    path('roster/<str:flight_number>/', get_flight_roster, name='flight-roster'),
    path('roster/<str:flight_number>/auto-assign/', auto_assign_crew, name='auto-assign-crew'),
]