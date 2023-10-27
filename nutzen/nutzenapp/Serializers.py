from rest_framework import serializers
from .models import User
class userserializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['user_id','username','email']