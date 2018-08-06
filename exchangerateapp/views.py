import sys

from django.db.models import Avg, Variance
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.views import APIView
import collections

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
    return ExchangeRate.objects.filter(date__range=(previous_date, rate_date), from_currency=from_curr,
                                      to_currency=to_curr).aggregate(Avg('rate_value'))

from collections import OrderedDict

def ordered_dict_prepend(dct, key, value, dict_setitem=dict.__setitem__):
    root = dct._OrderedDict__root
    first = root[1]

    if key in dct:
        link = dct._OrderedDict__map[key]
        link_prev, link_next, _ = link
        link_prev[1] = link_next
        link_next[0] = link_prev
        link[0] = root
        link[1] = first
        root[1] = first[0] = link
    else:
        root[1] = first[0] = dct._OrderedDict__map[key] = [root, first, key]
        dict_setitem(dct, key, value)

class GetExchangeLIst(ListCreateAPIView):
    queryset = ExchangeRate.objects.none()
    serializer_class = ExchangeRateSerializer

    def get_queryset(self):
        queryset = ExchangeRate.objects.all()
        return queryset

    @api_view(['GET'])
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

        average_dict = {er.from_currency.currency_code+'-'+er.to_currency.currency_code: get_rate_average(rate_date, previous_date, er.from_currency,
                                                             er.to_currency) for er in exchange_list}

        print(response_serializer.data)
        result_list =[]
        for d in response_serializer.data:
            d['average_val'] = average_dict[d['from_currency']+'-'+d['to_currency']]['rate_value__avg']
            result_list.append(d)

        return Response(result_list)

    @api_view(['GET'])
    def get_exchange_average(request):
        from_currency = request.query_params.get("from_currency")
        if not from_currency:
            return Response('Invalid from_currency parameter', status=status.HTTP_404_NOT_FOUND)
        to_currency = request.query_params.get("to_currency")
        if not to_currency:
            return Response('Invalid from_currency parameter', status=status.HTTP_404_NOT_FOUND)
        offset = request.query_params.get("offset")
        if not offset:
            return Response('Invalid Offset parameter', status=status.HTTP_404_NOT_FOUND)

        from_curr = Currency.objects.get(currency_code=from_currency)
        to_curr = Currency.objects.get(currency_code=to_currency)
        _vals ={'from_currency':from_curr,'to_currency':to_curr}
        from django.db.models import Q
        exchange_rate_list = ExchangeRate.objects.filter(Q(from_currency=from_curr) & Q(to_currency=to_curr)).order_by('-date')[:int(offset)]
        response_serializer = ExchangeRateSerializer(exchange_rate_list, many=True)
        avr_val = exchange_rate_list.aggregate(Avg('rate_value'))
        variance = exchange_rate_list.aggregate(Variance('rate_value'))

        aver_var = collections.OrderedDict()
        aver_var['average_val'] =avr_val
        aver_var['variance'] =variance
        data = response_serializer.data
        i =0
        dict_response ={}
        for d in data:
            i=i+1
            dict_response[i]=d

        dict_response[i+1]=aver_var
        print(data)
        return Response(dict_response)

    @api_view(['DELETE'])
    def delete_exchange(request):
        from_currency = request.query_params.get("from_currency")
        if not from_currency:
            return Response('Invalid from_currency parameter', status=status.HTTP_404_NOT_FOUND)
        to_currency = request.query_params.get("to_currency")
        if not to_currency:
            return Response('Invalid from_currency parameter', status=status.HTTP_404_NOT_FOUND)
        date = request.query_params.get("date")
        if not date:
            return Response('Invalid Date parameter', status=status.HTTP_404_NOT_FOUND)

        import datetime
        date_to_delete = datetime.strptime(date, "%Y-%m-%d").date()
        from_curr = Currency.objects.get(currency_code=from_currency)
        to_curr = Currency.objects.get(currency_code=to_currency)

        from django.db.models import Q
        ExchangeRate.objects.objects.filter(Q(from_currency=from_curr) & Q(to_currency=to_curr) & Q(date=date_to_delete)).delete()

        return Response("Deleted data",status=status.HTTP_200_OK)