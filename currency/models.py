from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.postgres.fields import ArrayField

ACCESS_LEVEL_CHOICES = [
    (1, "moderator"),
    (2, "user")
]

default_chosen_coins = ['btc', 'eth', 'usdt']

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        # Создание суперпользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
    
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, default='example_username')
    email = models.EmailField(max_length=100, default='example@mail.ru')
    password = models.CharField(max_length=50, default='12345678')
    register_time = models.DateTimeField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    chosen_coins = ArrayField(models.CharField(max_length=10), default=default_chosen_coins)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='user')
    last_login = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

class Currency(models.Model):
    name = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date_updated = models.DateTimeField(auto_now=True)
    difference = models.IntegerField()
    
    
    def __str__(self):
        return self.name


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    

