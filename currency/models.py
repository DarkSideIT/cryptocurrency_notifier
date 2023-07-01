from django.db import models

ACCESS_LEVEL_CHOICES = [
    (1, "moderator"),
    (2, "user")
]


class Currency(models.Model):
    name = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date_updated = models.DateTimeField(auto_now=True)
    difference = models.IntegerField()
    
    
    def __str__(self):
        return self.name
    
    
class User(models.Model):
    nickname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    register_time = models.DateTimeField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES)
    last_login = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.nickname
