from rest_framework import serializers
from .models import User,Offer
class userserializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['user_id','username','email']



class offer_serializers(serializers.ModelSerializer):
    class Meta:
        model=Offer
        fields='__all__'