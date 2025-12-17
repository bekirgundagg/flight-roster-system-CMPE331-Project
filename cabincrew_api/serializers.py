from rest_framework import serializers
from .models import CabinCrew, Language, ChefRecipe, VehicleType


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['lan_name']  # React'te .lan_name diye çağıracağız


class ChefRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefRecipe
        fields = ['recipe_name']


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['type_veh']  # React'te .type_veh diye çağıracağız


class CabinCrewSerializer(serializers.ModelSerializer):
    # Nested Serializers (İç içe veri çekme)
    known_languages = LanguageSerializer(many=True, read_only=True)
    recipes = ChefRecipeSerializer(many=True, read_only=True)

    # --- EKLENEN KISIM ---
    # Bunu eklemezsek sadece ID'ler gelir. Ekleyince isimler gelir.
    vehicle_restrictions = VehicleTypeSerializer(many=True, read_only=True)

    class Meta:
        model = CabinCrew
        fields = [
            'attendant_id',
            'name',
            'age',
            'gender',
            'nationality',
            'attendant_type',  # chief, regular, chef
            'seniority_level',
            'known_languages',
            'vehicle_restrictions',
            'recipes',
        ]