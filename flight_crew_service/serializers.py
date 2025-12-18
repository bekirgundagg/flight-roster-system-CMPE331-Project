from rest_framework import serializers
from .models import Pilot, Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language_name'] 

class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = [
            'id', 
            'name',
            'age',
            'gender',
            'nationality',
            'seniority_level',
            'allowed_range',
            'vehicle_restriction',
            'languages'  
        ]
        
        depth = 1

    def create(self, validated_data):
        instance = super().create(validated_data)
        
        language_ids = self.initial_data.get('languages')
        
        if language_ids:
            instance.languages.set(language_ids)
            
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        language_ids = self.initial_data.get('languages')
        if language_ids:
            instance.languages.set(language_ids)
            
        return instance

    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        return value