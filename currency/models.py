from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, BaseUserManager


from online_course_platform.settings import ALL_COINS, START_COINS


def default_chosen_coins():
    return START_COINS


ACCESS_LEVEL_CHOICES = [
    (1, "moderator"),
    (2, "user")
]


class User(AbstractUser):
    nickname = models.CharField(max_length=100, unique=True, default='example_username')
    email = models.EmailField(max_length=100, default='example@mail.ru')
    password = models.CharField(max_length=50, default='12345678')
    register_time = models.DateTimeField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    chosen_coins = ArrayField(models.CharField(max_length=10), default=default_chosen_coins)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='user')
    last_login = models.DateTimeField(auto_now=True)
    
    
    

class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, password = None, **extra_fields):
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        # Создание суперпользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class Currency(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    market_cup = models.CharField(max_length=50)
    difference = models.CharField(max_length=10)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
