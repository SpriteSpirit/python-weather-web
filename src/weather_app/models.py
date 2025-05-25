# Create your models here.
from django.db import models
from location_field.models.plain import PlainLocationField


class Place(models.Model):
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)