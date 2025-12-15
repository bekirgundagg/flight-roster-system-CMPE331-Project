# passengers/urls.py dosyası içinde

from rest_framework.routers import DefaultRouter
from .views import PassengerViewSet

# Router oluşturma
router = DefaultRouter()

# 'api/passengers' adresinde çalışacak API'yi kaydetme
router.register(r'passengers', PassengerViewSet, basename='passenger')

# Oluşturulan URL paternlerini projenin ana urls.py dosyasına gönderme
urlpatterns = router.urls