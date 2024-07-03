# weather/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeatherSerializer
from collections import defaultdict
from datetime import datetime
import statistics

class Weather(APIView):
    def get(self, request, city, *args, **kwargs):
        
        api_key = '8a2e5b5a178c85c8c41e7ceba8c5bc8a'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            daily_data = defaultdict(list)
            
            
            for item in data['list']:
                date_str = item['dt_txt']
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                day_of_week = date.strftime('%A')  
                
                forecast = {
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'description': item['weather'][0]['description']
                }
                daily_data[day_of_week].append(forecast)
            
            aggregated_forecast = []
            for day, forecasts in daily_data.items():
                temperatures = [forecast['temperature'] for forecast in forecasts]
                humidities = [forecast['humidity'] for forecast in forecasts]
                wind_speeds = [forecast['wind_speed'] for forecast in forecasts]
                descriptions = [forecast['description'] for forecast in forecasts]
                
            
                avg_temp = statistics.mean(temperatures)
                avg_humidity = statistics.mean(humidities)
                avg_wind_speed = statistics.mean(wind_speeds)
                most_common_desc = max(set(descriptions), key=descriptions.count)
                
                aggregated_forecast.append({
                    'day': day,
                    'humidity': avg_humidity,
                    'wind_speed': avg_wind_speed,
                    'description': most_common_desc
                })
            
            serializer = WeatherSerializer(aggregated_forecast, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)
