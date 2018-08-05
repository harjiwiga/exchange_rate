"""djangodocker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from exchangerateapp import views

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    url(r'^exchangerate/$', views.test_get,name='test_get'),
    url(r'^exchangerate/create/$', views.crate_exchange_rate,name='create'),
    url(r'^exchangerate/get_exchange_track/$', views.GetExchangeLIst.get_exchange_track,name='get_exchange_track'),
    # url(r'^exchangeRate/(?P<request>[\w-]+)', CreateView.test_get(),name="hello"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
