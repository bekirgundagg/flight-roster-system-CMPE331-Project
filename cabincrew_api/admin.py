from django.contrib import admin

from .models import CabinCrew, Language, VehicleType, ChefRecipe

admin.site.register(CabinCrew)
admin.site.register(Language)
admin.site.register(VehicleType)
admin.site.register(ChefRecipe)
