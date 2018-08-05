# from django.test import TestCase
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
#         self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
