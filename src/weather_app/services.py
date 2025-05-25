from typing import Optional

import requests
import os

from requests import Response

access_key = os.environ.get('API_KEY')

headers = {
    'X-Yandex-Weather-Key': access_key
}

def get_weather_info_by_point(lat: float, lon: float) -> Optional[Response]:
    """

    :param lat: ширина
    :param lon: долгота
    :return: ответ с данными о погоде
    """
    response = requests.get('https://api.weather.yandex.ru/v2/forecast?lat=52.37125&lon=4.89388', headers=headers)

    print(response.json())
