from rest_framework import serializers
from .models import CabinCrew, Language, ChefRecipe, VehicleType


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'lan_name'] #burada sadece lan name vardı unutma

class ChefRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefRecipe
        fields = ['recipe_name']


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'type_veh'] #buraya da id eklenmiş

class CabinCrewSerializer(serializers.ModelSerializer):
    known_languages = LanguageSerializer(many=True, read_only=True)
    recipes = ChefRecipeSerializer(many=True, read_only=True)
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

    def create(self, validated_data):
        instance = super().create(validated_data)

        language_ids = self.initial_data.get('known_languages')
        if language_ids:
            instance.known_languages.set(language_ids)

        vehicle_ids = self.initial_data.get('vehicle_restrictions')
        if vehicle_ids:
            instance.vehicle_restrictions.set(vehicle_ids)

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        language_ids = self.initial_data.get('known_languages')
        if language_ids:
            instance.known_languages.set(language_ids)

        vehicle_ids = self.initial_data.get('vehicle_restrictions')
        if vehicle_ids:
            instance.vehicle_restrictions.set(vehicle_ids)

        return instance

    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        return value