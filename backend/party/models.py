from django.db import models
from django.conf import settings
from argon2 import PasswordHasher

class Party(models.Model):
  host = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='host', on_delete=models.CASCADE) # 파티 호스트
  provider = models.ForeignKey('Provider', related_name='parties', on_delete=models.CASCADE)
  payments = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='payments', blank=True) # 결제를 한 파티원

  title = models.CharField(max_length=100) # 제목
  desc = models.TextField() # 상세 내용
  member_limit = models.IntegerField() # 모집 인원
  service_id = models.EmailField() # 서비스 계정
  service_password = models.CharField(max_length=100) # 비밀번호
  end_date = models.DateField() # 종료일
  price_per_day = models.PositiveIntegerField() # 하루 당 이용 요금
  
  def __str__(self):
    return self.title


class Provider(models.Model):
  name = models.CharField(max_length=20, unique=True)
  price_per_day = models.PositiveIntegerField(default=0)
  logo_url = models.CharField(max_length=100, default='')

  def __str__(self):
    return self.name

# class PartyPayment()