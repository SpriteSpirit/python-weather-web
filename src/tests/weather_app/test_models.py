import pytest
from django.db import IntegrityError, transaction

from weather_app.models import SearchHistory


@pytest.mark.django_db
def test_search_history_creation():
    """
    Тестирование создания записи истории поиска
    """

    city = SearchHistory.objects.create(city="Москва", latitude=55.7558, longitude=37.6176, search_count=5)

    assert city.city == "Москва"
    assert city.search_count == 5
    assert str(city) == "Москва (найден 5 раз)"


@pytest.mark.django_db
def test_unique_city_constraint():
    """
    Проверка уникальности города
    """

    SearchHistory.objects.create(city="Москва")

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            SearchHistory.objects.create(city="Москва")
