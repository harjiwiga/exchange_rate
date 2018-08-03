from django.db import models


# Create your models here.
class Country(models.Model):
    country_code = models.CharField(max_length=4)
    country_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


