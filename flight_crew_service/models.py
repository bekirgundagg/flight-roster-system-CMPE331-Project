from django.db import models
from django.core.validators import MinValueValidator

class Language(models.Model):
    # language_id (PK - Ana Anahtar) Django'll make it automaticlly
    language_name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.language_name

class Pilot(models.Model):
    SENIORITY_CHOICES = [
        ('senior', 'Senior Pilot'),
        ('junior', 'Junior Pilot'),
        ('trainee', 'Trainee'),
    ]

    name = models.CharField(max_length=100, null=False)

    age = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    gender = models.CharField(max_length=10, null=True, blank=True)

    nationality = models.CharField(max_length=50, null=True, blank=True)

    seniority_level = models.CharField(max_length=20, choices=SENIORITY_CHOICES, null=False, default='trainee')

    allowed_range = models.IntegerField(null=False)

    vehicle_restriction = models.CharField(max_length=50, null=False)

    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.name