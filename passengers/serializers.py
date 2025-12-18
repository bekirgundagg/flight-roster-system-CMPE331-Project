from rest_framework import serializers
from .models import Passenger

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        # '__all__' yerine alanları tek tek yazıyoruz ki
        # modeldeki @property olan 'full_name' ve 'is_infant' da gelsin.
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',  # Modeldeki @property sayesinde otomatik gelir
            'email',
            'age',
            'gender',
            'nationality',
            'flight_id',
            'seat_type',
            'seat_number',
            'is_infant',  # Modeldeki @property (True/False döner)
            'parent'
        ]