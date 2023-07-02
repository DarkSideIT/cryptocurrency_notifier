from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.utils import timezone


from online_course_platform.settings import START_COINS, ALL_COINS


from currency.models import User

from datetime import datetime
import json

params = ["", ""]

# Create your views here.
def home_view(request):
    return render(request, 'index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        nickname = request.POST.get("nickname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        chosen_coins = START_COINS
        register_time = timezone.now()
        balance = 0
        access_level = "user"
        try:
            user = User.objects.get(nickname=nickname)
            return render(request, 'index.html', {'error_message': 'Такой пользователь yже зарегистрирован!'})
        except User.DoesNotExist:
            user = User.objects.create(nickname=nickname, email=email, password=password, register_time=register_time, balance=balance, chosen_coins=chosen_coins, access_level=access_level)
            user.save()
            return render(request, 'index.html', {'success_message': 'Регистрация yспешна!'})
    
    else:
        return render(request)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        """email = body_data['email']"""
        """password = body_data['password']"""
        user = authenticate(request, email=email, password=password)
        if user is not None:
            django_login(request, user)
            return render(request, 'index.html', {'success_message': 'Вход yспешен!'})
        else:
            return render(request, 'index.html', {'success_message': 'Вход yспешен!'})
    
    else:
        return render(request)


def logout(request):
    django_logout(request)
    return redirect('login')

