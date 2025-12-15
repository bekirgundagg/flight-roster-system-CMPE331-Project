from rest_framework import viewsets
from .models import Pilot, Language
from .serializers import PilotSerializer, LanguageSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class PilotViewSet(viewsets.ModelViewSet):
    queryset = Pilot.objects.all().prefetch_related('languages')
    serializer_class = PilotSerializer