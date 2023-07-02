from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse ,HttpResponse
from django.db import connection
from django.middleware.csrf import get_token
from django.views import View


from online_course_platform.settings import ALL_COINS, START_COINS


from currency.models import Currency, User
from currency.handlers.parser import get_crypto_rank


from currency.registration.views import params
email = params[0]
password = params[1]

import json


coins = START_COINS


class CryptoQuotesView(View):
    template_name = 'index.html'
    
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
    def update_crypto_quotes(self):
        parsed_data = get_crypto_rank(['btc', 'eth', 'usdt'])
        for symbol, price, market_cap, difference in parsed_data.items():
            Currency.objects.create(symbol, price, market_cap, difference)
            
    
    def get_crypto_quotes(self):
        quotes = Currency.objects.all()
        data = []
        for quote in quotes:
            data.append({
                'name': quote.name,
                'price': quote.price,
                'market_cap': quote.market_cap,
                'difference': quote.difference
            })
        return data

    
    def dispatch(self, request, *args, **kwargs):
        self.update_crypto_quotes()
        if request.is_ajax():
            crypto_quotes = self.get_crypto_quotes()
            return JsonResponse(crypto_quotes, safe=False)
        return super().dispatch(request, *args, **kwargs)