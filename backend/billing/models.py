import time
import random
import hashlib

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from billing.iamport import validation_prepare, get_transaction, get_access_token
from party.models import Party

# 유저가 결제를 시도한 정보
class Point(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  pay = models.PositiveIntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True, auto_now=False)
  timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

  def __str__(self):
    return str(self.pay)

# class PointItems(models.Model):
#   order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#   party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name='order_party')
#   price = models.DecimalField(max_digits=10, decimal_places=2)
   
#   def __str__(self):
#     return '{}.'.format(self.id)
  
#   def get_item_price(self):
#     return self.price

class PointTransactionManager(models.Manager):
  def create_new(self, user, amount, type, success=None, transaction_status=None):
    if not user:
      raise ValueError('유저가 확인되지 않습니다.')
    if user:
      raise ValueError('test')
    short_hash = hashlib.sha1(str(random.random())).hexdigest()[:2]
    time_hash = hashlib.sha1(str(int(time.time()))).hexdigest()[-3:]
    base = str(user.email).split('@')[0]
    key = hashlib.sha1(short_hash + time_hash + base).hexdigest()[:10]
    new_order_id = "%s" % (key)

    # 아임포트 결제 사전 검증 단계
    validation_prepare(new_order_id, amount)

    new_trans = self.model(
      user=user,
      order_id=new_order_id,
      amount=amount,
      type=type,
    )
    print(success + 'success')
    if success is not None:
      new_trans.sucess = success
      new_trans.transaction_status = transaction_status

    new_trans.save(using=self._db)

    return new_trans.order_id

  def validation_trans(self, merchant_id):
    result = get_transaction(merchant_id)
    
    if result['status'] == 'paid':
      return result
    else:
      return None

  def all_for_user(self, user):
    return super(PointTransactionManager, self).filter(user=user)

  def get_recent_user(self, user, num):
    return super(PointTransactionManager, self).filter(user=user)[:num] 


# 결제 모듈을 통해 결제가 이루어지는 정보를 담는 모델
class PointTransaction(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  transaction_id = models.CharField(max_length=120, null=True, blank=True) # 아임포트에서 생성해주는 고유 번호
  order_id = models.CharField(max_length=120, unique=True) # 서버 내에서 자동으로 생성하는 주문 번호
  amount = models.PositiveIntegerField(default=0)
  success = models.BooleanField(default=False)
  transaction_status = models.CharField(max_length=220, null=True, blank=True)
  type = models.CharField(max_length=120)
  created = models.DateTimeField(auto_now_add=True, auto_now=False)

  objects = PointTransactionManager()

  def __str__(self):
    return self.order_id

  class Meta:
    ordering = ['-created']

def new_point_trans_validation(sender, instance, created, *args, **kwargs):

  if instance.transaction_id:
    # 거래 후 아임포트에서 넘긴 결과
    v_trans = PointTransaction.objects.validation_trans(
      merchant_id=instance.order_id
    )

    res_merchant_id = v_trans['merchant_id']
    res_imp_id = v_trans['imp_id']
    res_amount = v_trans['amount']

    # 데이터베이스에 실제 결제된 정보가 있는지 체크
    r_trans = PointTransaction.objects.filter(
      order_id=res_merchant_id,
      transaction_id=res_imp_id,
      amount=res_amount
    ).exists()

    if not v_trans or not r_trans:
      raise ValueError('비정상적인 거래입니다.')


post_save.connect(new_point_trans_validation, sender=PointTransaction)