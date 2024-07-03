from django.urls import path
from .views import Weather


urlpatterns = [
    path('weather/<str:city>/', Weather.as_view(), name='weather'),
]