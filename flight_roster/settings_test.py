from .settings import *
# from pathlib import Path  <-- Buna da gerek kalmadı çünkü sqlite dosya yolu oluşturmuyoruz
# BASE_DIR = ...            <-- Buna da gerek yok

# BURADAKİ DATABASES BLOĞUNU TAMAMEN SİLİYORUZ.
# Sildiğimizde otomatik olarak settings.py'deki MySQL ayarlarını kullanır.

# Bu kısım kalsın, testleri hızlandırır (Güvenliği düşürür ama test için iyidir)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]