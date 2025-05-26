from rest_framework import serializers

from .models import SearchHistory


class SearchHistoryStatSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения статистики поисковых запросов.
    Предоставляет название города и количество поисков.
    """

    class Meta:
        model = SearchHistory
        fields = ("city", "search_count")
