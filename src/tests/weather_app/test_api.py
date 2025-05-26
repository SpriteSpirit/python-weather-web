import pytest
from rest_framework.test import APIClient

from weather_app.models import SearchHistory


@pytest.mark.django_db
def test_search_stats_api():
    """
    Тест API статистики поиска
    """

    client = APIClient()
    SearchHistory.objects.create(city="Москва", search_count=5)

    response = client.get("/api/stats/")

    assert response.status_code == 200
    assert response.data[0]["city"] == "Москва"
    assert response.data[0]["search_count"] == 5
