from rest_framework import serializers
from .models import CabinCrew, Language, ChefRecipe, VehicleType

class LanguageSerializer(serializers.ModelSerializer):
    """ converting to JSON """
    class Meta:
        model = Language
        fields = ['lan_name']

class ChefRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChefRecipe
        fields = ['recipe_name']

class VehicleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleType
        fields = ['type_veh']

class CabinCrewSerializer(serializers.ModelSerializer):

    known_languages = LanguageSerializer (many=True, read_only=True)
    recipes = ChefRecipeSerializer (many=True, read_only=True)

    class Meta:
        model = CabinCrew
        fields = [
            'attendant_id',
            'name',
            'age',
            'gender',
            'nationality',
            'attendant_type',
            'senority_level',
            'known_languages',
            'vehicle_restrictions',
            'recipes',
        ]