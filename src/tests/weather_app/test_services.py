from unittest.mock import patch

import requests

from weather_app import services


@patch("weather_app.services.requests.get")
def test_get_coordinates_success(mock_get):
    """
    Тест успешного получения координат
    """

    mock_response = {
        "response": {
            "GeoObjectCollection": {
                "featureMember": [
                    {
                        "GeoObject": {
                            "Point": {"pos": "37.6176 55.7558"},
                            "name": "Москва",
                            "metaDataProperty": {
                                "GeocoderMetaData": {
                                    "Address": {"Components": [{"kind": "locality", "name": "Москва"}]}
                                }
                            },
                        }
                    }
                ]
            }
        }
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    result = services.get_coordinates("Москва")
    assert result == (55.7558, 37.6176, "Москва")


@patch("weather_app.services.requests.get")
def test_get_coordinates_failure(mock_get):
    """
    Тест ошибки при получении координат
    """

    mock_get.side_effect = requests.exceptions.RequestException
    assert services.get_coordinates("Несуществующий город") is None
