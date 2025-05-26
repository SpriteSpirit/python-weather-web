import logging
from typing import Any

import requests
from django.conf import settings

GEOCODER_API_URL = "https://geocode-maps.yandex.ru/1.x/"
WEATHER_API_URL = "https://api.weather.yandex.ru/v2/forecast"

logger = logging.getLogger("weather_app")


def get_coordinates(city_name: str) -> tuple[float, float, str] | None:
    """
    Получает координаты и нормализованное название города.
    :param city_name: Название города.
    :return: Кортеж (широта, долгота, нормализованное название) или None.
    """

    params = {
        "apikey": settings.YANDEX_GEOCODER_KEY,
        "geocode": city_name,
        "format": "json",
        "results": 1,
        "kind": "locality",
        "lang": "ru_RU",
    }

    try:
        response = requests.get(GEOCODER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        features = data.get("response", {}).get("GeoObjectCollection", {}).get("featureMember", [])

        if not features:
            logger.warning(f"Geocoder: не найдены объекты для города '{city_name}'")
            return None

        geo_object = features[0].get("GeoObject", {})

        if not geo_object:
            logger.error(f"Geocoder: отсутствует GeoObject для города '{city_name}'")
            return None

        point = geo_object.get("Point", {})
        pos = point.get("pos")

        if not pos:
            logger.error(f"Geocoder: отсутствуют координаты (pos) для города '{city_name}'")
            return None

        longitude, latitude = map(float, pos.split())
        normalized_city = geo_object.get("name")

        meta_data = geo_object.get("metaDataProperty", {}).get("GeocoderMetaData", {})
        components = meta_data.get("Address", {}).get("Components", [])

        for comp in components:
            if comp.get("kind") == "locality":
                normalized_city = comp.get("name")
                break

        if not normalized_city:
            try:
                address_details = meta_data.get("AddressDetails", {})
                country = address_details.get("Country", {})
                admin_area = country.get("AdministrativeArea", {})
                locality = admin_area.get("Locality", {})
                loc_name = locality.get("LocalityName")

                if loc_name:
                    normalized_city = loc_name
            except Exception:
                logger.warning(f"Не удалось получить LocalityName для города '{city_name}'.")

        if not normalized_city:
            normalized_city = geo_object.get("name")

        if not normalized_city:
            logger.error(f"Geocoder: не удалось определить название города '{city_name}'. Ответ: {data}")
            return None

        logger.info(f"Geocoder:  найдено '{normalized_city}' ({latitude}, {longitude}) для ввода '{city_name}'")

        return latitude, longitude, normalized_city

    except requests.RequestException as e:
        logger.error(f"Geocoder RequestException: {str(e)}")

        return None
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Geocoder ошибка парсинга: {type(e).__name__} - {str(e)}")

        return None


def get_weather_forecast(lat: float, lon: float) -> dict[str, Any] | None:
    """
    Получает прогноз погоды по координатам.
    :param lat: Широта в градусах.
    :param lon: Долгота в градусах.
    :return: Словарь с данными погоды от API или None в случае ошибки.
    """

    headers = {"X-Yandex-API-Key": settings.YANDEX_WEATHER_KEY}
    params = {"lat": lat, "lon": lon, "lang": "ru_RU", "limit": 3}

    try:
        response = requests.get(WEATHER_API_URL, headers=headers, params=params)
        response.raise_for_status()

        return response.json()
    except requests.RequestException as e:
        logger.error(f"Ошибка API: {e}")

        return None
