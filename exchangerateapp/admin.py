from django.contrib import admin
from .models import Country, Currency, ExchangeRate

admin.register(Country)
admin.register(Currency)
admin.register(ExchangeRate)
# Register your models here.
