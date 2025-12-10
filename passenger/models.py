from django.db import models

# Create your models here.
# passenger/models.py dosyası içinde

from django.db import models

class Passenger(models.Model):
    # Yolcu adı, 100 karakter sınırıyla
    first_name = models.CharField(max_length=100)
    # Yolcu soyadı, 100 karakter sınırıyla
    last_name = models.CharField(max_length=100)
    # E-posta adresi, veritabanında benzersiz olmalı
    email = models.EmailField(unique=True)
    
    def __str__(self):
        # Yönetici panelinde kolay tanıma için
        return f"{self.first_name} {self.last_name}"