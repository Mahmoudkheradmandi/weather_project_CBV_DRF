# weather/serializers.py
from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    
    day = serializers.CharField(max_length=10)
    humidity = serializers.FloatField()
    wind_speed = serializers.FloatField()
    description = serializers.CharField(max_length=100)
