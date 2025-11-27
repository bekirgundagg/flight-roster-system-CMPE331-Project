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
        
        # "depth = 1" ayarı, serializer'a şunu der:
        # "languages" gibi ilişkili alanları (ForeignKey, ManyToMany)
        # işlerken, sadece ID'lerini verme. Bir seviye derine in
        # ve o objelerin (Language) tüm bilgilerini getir.
        depth = 1