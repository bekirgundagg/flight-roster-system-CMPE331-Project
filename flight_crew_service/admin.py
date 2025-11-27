from django.contrib import admin
from .models import Pilot, Language  # 1. Adım: models.py'dan modellerimizi import etme işi

# 2. Adım: Bu modelleri admin paneline kaydetme işi
admin.site.register(Pilot)
admin.site.register(Language)