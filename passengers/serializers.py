from rest_framework import serializers
from .models import Passenger

class PassengerSerializer(serializers.ModelSerializer):
    # Ebeveyn ismini özel olarak çekmek için bir metod alanı ekliyoruz.
    # Bu sayede frontend'e sadece ID değil, isim de gidecek.
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Passenger
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',  # Modeldeki @property
            'email',
            'age',
            'gender',
            'nationality',
            'flight_id',
            'seat_type',
            'seat_number',
            'is_infant',  # Modeldeki @property
            'parent',     # Bu alan ebeveynin ID'sini (örn: 5) döndürür (Backend işlemleri için gerekli)
            'parent_name' # Bu alan ebeveynin İSMİNİ (örn: "Ali Yılmaz") döndürür (Frontend gösterimi için) <--- YENİ
        ]

    def get_parent_name(self, obj):
        """
        Her bir yolcu objesi için çalışır.
        Eğer yolcunun bir ebeveyni (parent) varsa, o ebeveynin tam adını döndürür.
        Yoksa (yetişkinse veya ebeveyni yoksa) None döndürür.
        """
        if obj.parent:
            return obj.parent.full_name
        return None