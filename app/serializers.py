from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
import shortuuid
import random

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username=serializers.CharField(required=True)
    referid=serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username","email", "password", "first_name", "last_name","referid","referredid","date_joined"]  # Include the username field in fields list
        extra_kwargs = {"id": {"read_only": True},"email":{"required":True},"password":{"required":True}}
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        # validated_data["username"]=validated_data.get('email') 
        s = shortuuid.ShortUUID(alphabet="0123456789")
        reid = s.random(length=5)
        referid="RF"+str(reid)
        validated_data["referid"]=referid
        referredid = validated_data.get('referredid')
        if referredid:
            # Assuming 'User' is the model name
            referred_user_exists = User.objects.filter(referid=referredid).exists()
            if not referred_user_exists:
                raise serializers.ValidationError({"referredid": "Invalid referred ID"})
        return super().create(validated_data)

class ReferralSerailizer(serializers.ModelSerializer):
    class Meta:
        model=User