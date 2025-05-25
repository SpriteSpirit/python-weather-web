from django.urls import path

from weather_app.apps import WeatherAppConfig
from weather_app.views import WeatherAppView

app_name = WeatherAppConfig.name

urlpatterns = [
    path('', WeatherAppView.as_view(), name='weather'),
]
