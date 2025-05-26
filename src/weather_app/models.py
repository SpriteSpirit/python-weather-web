from django.db import models

NULLABLE = {"null": True, "blank": True}


class SearchHistory(models.Model):
    """
    Модель для хранения истории поиска погоды по городам.
    """

    # Если нужно привязать к пользователю:
    # user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Пользователь")

    city = models.CharField(max_length=100, verbose_name="Название населенного пункта")
    latitude = models.FloatField(verbose_name="Широта", **NULLABLE)
    longitude = models.FloatField(verbose_name="Долгота", **NULLABLE)
    search_count = models.PositiveIntegerField(default=1, verbose_name="Количество запросов")
    last_searched = models.DateTimeField(auto_now=True, verbose_name="Последний поиск")

    class Meta:
        """
        Дополнительные настройки модели.
        """

        verbose_name = "Запись истории поиска"
        verbose_name_plural = "История поисковых запросов"
        unique_together = ("city",)
        ordering = ["-last_searched"]
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["last_searched"]),
        ]

    def __str__(self):
        return f"{self.city} (найден {self.search_count} раз)"
