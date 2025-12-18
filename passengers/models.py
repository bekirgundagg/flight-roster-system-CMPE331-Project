from django.db import models
from django.core.validators import MinValueValidator

class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    SEAT_TYPE_CHOICES = [
        ('business', 'Business'),
        ('economy', 'Economy'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(unique=True, null=True, blank=True)

    age = models.IntegerField(
        verbose_name="Yaş", 
        default=25, 
        validators=[MinValueValidator(0)]
    )  
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Cinsiyet", default='O')
    nationality = models.CharField(max_length=50, verbose_name="Milliyet", default="Unknown")

    flight_id = models.CharField(max_length=10, verbose_name="Uçuş Numarası (Flight ID)")

    seat_type = models.CharField(max_length=10, choices=SEAT_TYPE_CHOICES, default='economy',
                                 verbose_name="Koltuk Tipi")
    seat_number = models.CharField(max_length=5, null=True, blank=True, verbose_name="Koltuk No")

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='infants',
                               verbose_name="Ebeveyn (Bebekler için)")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.flight_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_infant(self):
        """0-2 yaş arası bebek mi kontrolü"""
        return self.age <= 2