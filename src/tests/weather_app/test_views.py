import pytest

from weather_app.models import SearchHistory


@pytest.mark.django_db
def test_weather_view_get(client):
    """
    Тест GET-запроса к WeatherView
    """

    response = client.get("/")
    assert response.status_code == 200
    assert "yandex_geo_api_key" in response.context


@pytest.mark.django_db
def test_weather_view_post_valid(client, mocker):
    """
    Тест успешного POST-запроса
    """

    mocker.patch("weather_app.services.get_coordinates", return_value=(55.7558, 37.6176, "Москва"))
    mocker.patch("weather_app.services.get_weather_forecast", return_value={"fact": {}})

    response = client.post("/", {"city": "Москва"})
    assert response.status_code == 200
    assert "Москва" in response.content.decode()


@pytest.mark.django_db
def test_search_history_update(client, mocker):
    """
    Тест обновления истории поиска
    """

    mocker.patch("weather_app.services.get_coordinates", return_value=(55.7558, 37.6176, "Москва"))
    mocker.patch("weather_app.services.get_weather_forecast", return_value={"fact": {}})

    # Первый запрос
    client.post("/", {"city": "Москва"})
    # Второй запрос
    client.post("/", {"city": "Москва"})

    history = SearchHistory.objects.get(city="Москва")
    assert history.search_count == 2
