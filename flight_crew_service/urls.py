from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views 

router = DefaultRouter()

router.register(r'pilots', views.PilotViewSet, basename='pilot')

router.register(r'languages', views.LanguageViewSet, basename='language')

urlpatterns = [
    path('', include(router.urls)),
]