import logging

from django.db import transaction
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings

from . import services
from .models import SearchHistory
from .serializers import SearchHistoryStatSerializer

logger = logging.getLogger("weather_app")


class WeatherView(View):
    """
    Обрабатывает отображение и обработку запросов для получения прогноза погоды.
    """

    template_name = "weather_app/index.html"

    def get(self, request):
        """
         Отображает главную страницу с формой поиска погоды.
        :param request: HTTP-запрос.
        :return: Страница с формой поиска и последним сохраненным городом.
        """

        last_city = request.session.get("last_city")

        context = {
            "yandex_geo_api_key": settings.YANDEX_GEOCODER_KEY,
            "yandex_suggest_key": settings.YANDEX_SUGGEST_KEY,
        }

        if last_city:
            context["last_city"] = last_city

        return render(request, self.template_name, context)

    def post(self, request):
        """
        Обрабатывает запрос на получение прогноза погоды.
        :param request: HTTP-запрос с параметром 'city'.
        :return: Страница с результатами поиска или сообщением об ошибке.
        :raises: Страница с ошибкой при пустом вводе, отсутствии координат, ошибке получения прогноза.
        """

        city_input = request.POST.get("city", "").strip()

        if not city_input:
            return render(request, self.template_name, {"error": "Название города не может быть пустым."})

        result = services.get_coordinates(city_input)

        if not result:
            return render(request, self.template_name, {"error": f'Город "{city_input}" не найден'})

        lat, lon, normalized_city = result
        forecast_data = services.get_weather_forecast(lat, lon)

        if not forecast_data:
            return render(
                request, self.template_name, {"error": "Не удалось получить прогноз погоды. Попробуйте позже."}
            )

        try:
            with transaction.atomic():
                history_entry, created = SearchHistory.objects.get_or_create(
                    city__iexact=normalized_city,
                    defaults={"city": normalized_city, "latitude": lat, "longitude": lon},
                )
                if not created:
                    history_entry.search_count += 1
                    history_entry.save(update_fields=["search_count", "last_searched"])
        except Exception as e:
            logger.error(f"Ошибка сохранения истории: {str(e)}")

        request.session["last_city"] = normalized_city

        context = {
            "city": normalized_city,
            "forecast": forecast_data,
            "now": forecast_data.get("fact", {}),
            "days": forecast_data.get("forecasts", []),
            "search_history": SearchHistory.objects.order_by("-last_searched")[:5],
            "yandex_suggest_key": settings.YANDEX_SUGGEST_KEY,
        }

        return render(request, self.template_name, context)


class SearchStatsAPIView(APIView):
    """
    API для получения статистики поисковых запросов.
    Предоставляет данные в формате JSON, отсортированные по количеству поисков.
    """

    def get(self, request):
        """
        Возвращает статистику поисковых запросов.
        :param request: HTTP-запрос.
        :return: JSON-ответ с данными статистики.
        """

        stats = SearchHistory.objects.order_by("-search_count")
        serializer = SearchHistoryStatSerializer(stats, many=True)

        return Response(serializer.data)
