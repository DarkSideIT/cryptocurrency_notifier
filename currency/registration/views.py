from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from currency.models import EmailBackend
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.utils import timezone
from django.contrib.auth.models import Permission


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
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        chosen_coins = START_COINS
        register_time = timezone.now()
        balance = 0
        access_level = "user"
        try:
            user = User.objects.get(username=username)
            return render(request, 'index.html', {'error_message': 'Такой пользователь yже зарегистрирован!'})
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email, password=password, register_time=register_time, balance=balance, chosen_coins=chosen_coins, access_level=access_level)
            user.save()
            user = User.objects.get(username='username')
            permission = Permission.objects.get(codename='change_post')
            user.user_permissions.add(permission)
            return render(request, 'index.html', {'success_message': 'Регистрация yспешна!'})
    
    else:
        return render(request)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        email_backend = EmailBackend()
        user = email_backend.authenticate(request, username=email, password=password)
        if user is not None:
            django_login(request, user)
            return render(request, 'index.html', {'success_message': 'Вход yспешен!'})
        else:
            return render(request, 'index.html', {'error_message': 'Вход yспешен!'})
    
    else:
        return render(request)


def logout(request):
    django_logout(request)
    return redirect('login')

