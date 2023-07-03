from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.db import connection


from currency.models import User

from datetime import datetime
import json

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        nickname = body_data["nickname"]
        email = body_data["email"]
        password = body_data["password"]
        register_time = datetime.now()
        balance = 0
        access_level = "user"
        try:
            user = User.objects.get(nickname=nickname)
            return JsonResponse({"message": "this user already exists"})
        except User.DoesNotExist:
            user = User.objects.create(nickname=nickname, email=email, password=password, register_time=register_time, balance=balance, access_level=access_level)
            user.save()
            return JsonResponse({"message": "user is saved"})
    
    else:
        return render(request)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data['email']
        password = body_data['password']
        query = "select * from currency_user where email=%s and password=%s"
        params = [email, password]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        
        if result:
            user = User.objects.get(email=email)
            django_login(request, user)
            return JsonResponse({"message": "you are logged"})
        else: 
            return JsonResponse({"message": "incorrect data"})
    
    else:
        return render(request)


def logout(request):
    django_logout(request)
    return redirect('login')