from django.db.models import fields
from .models import Party, Provider
from sign.models import User
from rest_framework import serializers
from sign.serializers import UserSerializer, UserSmallSerializer
# from argon2 import PasswordHasher
from django.contrib.auth import get_user_model


# 
class MyPartySerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Party
    fields = ('id',)

class PartySmallSerializer(serializers.ModelSerializer):
  payments = UserSerializer()

  class Meta:
    model = Party
    fields = ('id', 'payments',)
    depth = 1
  
# 로그인 되어 있는 유저 모델을 가져온다.
class HostUserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = get_user_model()
    fields = ['id', 'nick_name']
# 결제 유저 모델
class PaymentsUserSerializer(serializers.ModelSerializer):
  payments = UserSmallSerializer(required=False, many=True)

  class Meta:
    model = Party
    fields = ('id', 'payments',)

class PartyCreateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Party
    fields = ('title', 'desc', 'service_id', 'service_password', 'member_limit', 'end_date', 'price_per_day')


class PartySerializer(serializers.ModelSerializer):
  payments = UserSmallSerializer(required=False, many=True)
  host = HostUserSerializer()

  class Meta:
    model = Party
    fields = '__all__'
    depth = 1


class ProviderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Provider
    fields = '__all__'


