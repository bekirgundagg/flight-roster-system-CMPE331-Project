from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CabinCrewViewSet, VehicleTypeViewSet, ChefRecipeViewSet 

router = DefaultRouter()

router.register(r'crew', CabinCrewViewSet)
router.register(r'vehicles', VehicleTypeViewSet)
router.register(r'recipes', ChefRecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]