from rest_framework import serializers

from .models import Currency, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:

        model = Currency()
        fields = ('currency_code', 'currency_name')
        # read_only_fields = ('currency_code', 'currency_name')


class ExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRate()
        fields = ('id', 'date', 'from_currency', 'to_currency', 'rate_value')


class ExchangeRateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        exchange_rate = [ExchangeRateSerializer(**item) for item in validated_data]
        return ExchangeRate.objects.bulk_create(exchange_rate)

