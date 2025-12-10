from django.db import models


class Passenger(models.Model):
    # Seçenekler (Choices) - Veri tutarlılığı için
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    SEAT_TYPE_CHOICES = [
        ('business', 'Business'),
        ('economy', 'Economy'),
    ]

    # --- Kimlik Bilgileri ---
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    # Dokümanda email zorunlu değil ama kalabilir, opsiyonel yaptım.
    email = models.EmailField(unique=True, null=True, blank=True)

    # --- Dokümanda İstenen Zorunlu Alanlar [Kaynak: 71] ---
    age = models.IntegerField(verbose_name="Yaş", default=25)  # Varsayılan değer hata almanı engeller
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Cinsiyet", default='O')
    nationality = models.CharField(max_length=50, verbose_name="Milliyet", default="Unknown")

    # --- Uçuş ve Koltuk Bilgileri [Kaynak: 69, 71, 73] ---
    # Uçuş numarası (AANNNN formatında string tutulabilir veya Flight modeline ForeignKey yapılabilir)
    # Şimdilik string olarak tutuyoruz çünkü microservice mimarisinde ID gelir.
    flight_id = models.CharField(max_length=10, verbose_name="Uçuş Numarası (Flight ID)")

    seat_type = models.CharField(max_length=10, choices=SEAT_TYPE_CHOICES, default='economy',
                                 verbose_name="Koltuk Tipi")
    seat_number = models.CharField(max_length=5, null=True, blank=True, verbose_name="Koltuk No")

    # --- Bebek Yolcular İçin Ebeveyn Bilgisi [Kaynak: 72] ---
    # Eğer yolcu bebekse (0-2 yaş), bir ebeveyni olmalı. Kendi tablosuna referans veriyoruz.
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