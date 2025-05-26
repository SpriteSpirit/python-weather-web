from django.urls import path

from weather_app.apps import WeatherAppConfig
from weather_app.views import SearchStatsAPIView, WeatherView

app_name = WeatherAppConfig.name

urlpatterns = [
    path("", WeatherView.as_view(), name="weather"),
    path("api/stats/", SearchStatsAPIView.as_view(), name="search_stats_api"),
]
