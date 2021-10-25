from django.conf import settings
from django.db import transaction
from django.db.models import fields
from party.models import Party, Provider

from rec_movie.serializers import GenreSerializer as MovieGenreSerializer
from rec_program.serializers import GenreSerializerP as ProgramGenreSerializer
from .models import User
from rec_movie.serializers import GenreSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import (
  UserDetailsSerializer, LoginSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSmallSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'nick_name', 'username', 'email', 'phone_number')

class ProviderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Provider
    fields = '__all__'


class PartySmallSerializer(serializers.ModelSerializer):
  host = UserSmallSerializer()
  provider = ProviderSerializer()
  
  class Meta:
    model = Party
    exclude = ('payments',)

class UserSerializer(serializers.ModelSerializer):
  payments = PartySmallSerializer(required=False, many=True)
  fav_movie_genres = MovieGenreSerializer(required=False, many=True)
  fav_program_genres = ProgramGenreSerializer(required=False, many=True)

  class Meta:
    model = User
    exclude = ('password', 'last_login', 'is_active', 'is_admin')

class UserLoginSerializer(LoginSerializer):

  class Meta:
    model = User
    fields = ['email', 'password',]


class UserRegisterSerializer(RegisterSerializer):
  phone_number = serializers.CharField(max_length=20)
  nick_name = serializers.CharField(max_length=100)
  password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'password2', 'phone_number', 'nick_name',]
    extra_kwarge= {
      'password': {
        'write_only': True
      }
    }
  def save(self, request):
    user = User(
      username = self.validated_data['username'],
      email = self.validated_data['email'],
      nick_name = self.validated_data['nick_name'],
      phone_number = self.validated_data['phone_number'],
    )
    password1 = self.validated_data['password1']
    password2 = self.validated_data['password2']

    if password1 != password2:
      raise serializers.ValidationError({'password': 'Passwords must match.'})
    user.set_password(password1)
    user.save()
    return user


class UserDetailSerializer(UserDetailsSerializer):
  payments = PartySmallSerializer(required=False, many=True)
  fav_movie_genres = MovieGenreSerializer(required=False, many=True)
  fav_program_genres = ProgramGenreSerializer(required=False, many=True)
  class Meta:
    model = User
    fields = (
      'id',
      'username',
      'email',
      'nick_name',
      'phone_number',
      'fav_movie_genres',
      'fav_program_genres',
      'payments',
    )
    read_only_fields = ('id', 'email', 'username')

class UserGenreSerializer(serializers.ModelSerializer):
  fav_movie_genres = MovieGenreSerializer(required=False, many=True)
  fav_program_genres = ProgramGenreSerializer(required=False, many=True)

  class Meta:
    model = User
    fields = ( 'fav_movie_genres', 'fav_program_genres' )
