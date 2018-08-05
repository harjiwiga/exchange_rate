from django.test import TestCase
from .models import Currency,ExchangeRate

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):
        self.currency_code = "IDR"
        self.currency = Currency(currency_code="IDR")

    def test_model_and_create_currency(self):
        old_count = Currency.objects.count()
        self.currency.save()
        print("test the currency model")
        new_count = Currency.objects.count()
        print(new_count)
        self.assertNotEqual(old_count,new_count)

    def test_unique_currency_model(self):
        idr = Currency()
        idr.currency_code="IDR"
        idr.save()
        usd = Currency()
        usd.currency_code="IDR"
        self.assertEqual(Currency.objects.count, 1)
        self.assertNotEqual(idr.currency_code,usd.currency_code)
    
    def test_create_model_exchange_rate(self):
        usd_to_idr = ExchangeRate()
        
# from rest_framework.test import APIClient
# from rest_framework import status
# from django.urls import reverse


# class ViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.exchange_rate_data = {'date': '2018-08-01', 'from_currency': 'USD',
#                                    'to_currency': 'IDR', 'rate_value': '14497.1470905164'}
#         self.response = self.client.post(reverse('create'),
#                                          self.exchange_rate_data,
#                                          format="json")

#     def test_api_can_create_exchange_rate(self):
#         print ("view test case")
#         self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

