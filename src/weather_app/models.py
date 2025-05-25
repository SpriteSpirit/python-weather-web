# Create your models here.

from django.db import models
from location_field.models.plain import PlainLocationField

NULLABLE = {'null': True, 'blank': True}


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название города')
    location = PlainLocationField(
        based_fields=['name'],
        zoom=7,
        verbose_name="Город на карте")

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
