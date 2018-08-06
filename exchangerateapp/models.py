from django.db import models


# Create your models here.
class Country(models.Model):
    country_code = models.CharField(max_length=4)
    country_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        self.country_name


class Currency(models.Model):
    currency_code = models.CharField(max_length=4, unique=True, primary_key=True)
    currency_name = models.CharField(max_length=100)

    def __str__(self):
        self.currency_code
class AverageVal:
    def __init__(self,average_val):
        self.average_val =average_val
    def __str__(self):
        return self.average_val

class ExchangeRate(models.Model):

    class Meta:
        unique_together = (('from_currency', 'to_currency', 'date'),)

    date = models.DateField(auto_now=False, null=False)
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='%(class)s_from_currency')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='%(class)s_to_currency')
    rate_value = models.DecimalField(max_digits=18, decimal_places=10)

    # def __str__(self):
    #     field_values = []
    #     for field in self._meta.get_all_field_names():
    #         field_values.append(getattr(self, field, ''))
    #     return ' '.join(field_values)

    # def average_val(obj):
    #     return obj
