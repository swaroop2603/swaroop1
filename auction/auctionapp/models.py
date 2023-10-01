from django.db import models
from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput
class User(models.Model):
    
    id=models.IntegerField(primary_key=True,auto_created=True)
    name=models.CharField(max_length=100,unique=True)
    email=models.EmailField()
    password = models.CharField(max_length=10)


    def __str__(self):
        return self.User