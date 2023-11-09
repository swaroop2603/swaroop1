from django.db import models
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)




class Offer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    offer_type = models.CharField(max_length=50)
    amount=models.IntegerField()
    start_date=models.DateTimeField(null=True, blank=True)
    end_date=models.DateTimeField(null=True, blank=True)
    description=models.TextField()
