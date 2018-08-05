import sys
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.views import APIView

from .models import ExchangeRate, Currency
from .model_serializer import ExchangeRateSerializer, ExchangeRateListSerializer

query_set = ExchangeRate.objects.all()
serializer_class = ExchangeRateSerializer


@api_view(['GET'])
def test_get(request):
    print("request:", request.query_params.get("q"))
    return Response({"message": "Hello, world!"})


@api_view(['POST'])
@parser_classes((JSONParser,))
def crate_exchange_rate(request):
    request_data = request.data
    date = request_data['date']
    from_currency = request_data['from_currency']
    to_currency = request_data['to_currency']
    rate_value = request_data['rate_value']
    exchange_rate_ls = ExchangeRate.objects.filter(date=date, from_currency=from_currency, to_currency=to_currency)
    exchange_rate = ExchangeRate()
    if exchange_rate_ls:
        exchange_rate = exchange_rate_ls[0]
        exchange_rate.rate_value = rate_value
    else:
        from_curr = Currency.objects.get(currency_code=from_currency)
        to_curr = Currency.objects.get(currency_code=to_currency)
        exchange_rate.date = date
        exchange_rate.from_currency = from_curr
        exchange_rate.to_currency = to_curr
        exchange_rate.rate_value = rate_value
    exchange_rate.save()

    return Response(ExchangeRateSerializer(exchange_rate).data, status=status.HTTP_200_OK)


def get_rate_average(rate_date, previous_date, from_curr, to_curr):
    from django.db.models import Avg
    return ExchangeRate.object.filter(date_range=(previous_date, rate_date), from_currency=from_curr,
                                      to_currency=to_curr).aggregate(Avg('rate_value'))


class GetExchangeLIst(ListCreateAPIView):
    queryset = ExchangeRate.objects.none()
    serializer_class = ExchangeRateSerializer

    def get_queryset(self):
        queryset = ExchangeRate.objects.all()
        return queryset

    @api_view(['GET'])
    # @parser_classes((JSONParser,))
    def get_exchange_track(request):
        print("request_data", request.query_params)
        rate_date = request.query_params.get("date")
        if not rate_date:
            return Response('Invalid Date parameter', status=status.HTTP_404_NOT_FOUND)
        offset = request.query_params.get("offset")
        if not offset:
            return Response('Invalid Offset parameter', status=status.HTTP_404_NOT_FOUND)
        from datetime import datetime, timedelta

        previous_date = datetime.strptime(rate_date, "%Y-%m-%d").date() - timedelta(days=int(offset))

        exchange_list = ExchangeRate.objects.filter(date=rate_date)
        response_serializer = ExchangeRateSerializer(exchange_list, many=True)

        average_dict = {exchange_rate.date: get_rate_average(rate_date, previous_date, exchange_rate['from_currency'],
                                                             exchange_rate['to_currency']) for exchange_rate in
                        exchange_list}
        # response_serializer.average_value(0)

        print(average_dict)
        return Response(response_serializer.data)
