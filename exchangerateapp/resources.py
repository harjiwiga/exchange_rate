from tastypie.resources import ModelResource
from .models import ExchangeRate

class ExchangeRateResource(ModelResource):
    class Meta:
        queryset = ExchangeRate.objects.all()
        resource_name ='exchange_rate'