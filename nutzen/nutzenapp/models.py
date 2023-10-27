from django.db import models
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)