from typing import Optional, Tuple

import requests
import os

from django.test import AsyncClient

from weather_app.models import City

access_key = os.environ.get('API_KEY')


async def get_yandex_weather(lat: float, lon: float) -> Optional[dict]:
    """
    Запрос к API Яндекс Погоды

    :param lat: Широта
    :param lon: Долгота
    :return: Данные о погоде в формате json или None в случае ошибки
    """

    async with AsyncClient() as client:
        url = "https://api.weather.yandex.ru/v2/forecast?"
        headers = {
            'X-Yandex-Weather-Key': access_key
        }
        params = {
            'lat': lat,
            'lon': lon,
            'lang': 'ru_RU',
            'limit': 1,
            'hours': False
        }

        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()

            print(response.json())
            return response.json()
        except requests.HTTPError as e:
            print(f'Ошибка запроса к API Яндекс.Погода: {e}')
            return None


def get_city_coordinates_by_name(city_name: str) -> Optional[Tuple[float, float]]:
    """
    Получение координат из модели города City

    :param city_name: Название города
    :return: Кортеж из широты и долготы или None в случае ошибки
    """

    try:
        city = City.objects.get(name=city_name)
        lat, lon = map(float, city.location.split(','))

        return lat, lon
    except (City.DoesNotExist, ValueError, AttributeError):
        return None
