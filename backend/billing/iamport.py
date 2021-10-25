import requests
import json

from django.conf import settings
# 아임포트 서버에 접근할 수 있는 토큰을 받는 과정
def get_access_token():
  access_data = {
    'imp_key': settings.IAMPORT_KEY,
    'imp_secret': settings.IAMPORT_SECRET
  }
  print(access_data)
  url = 'https://api.iamport.kr/users/getToken'
  req = requests.post(url, data=access_data)
  access_res = req.json()

  if access_res['code'] is 0:
    return access_res['response']['access_token']
  else:
    return None

# 결제를 검증하는 단계 (유저가 요청한 금액과 아임포트에 있는 결제 금액이 일치하는지 검증)
def validation_prepare(merchant_id, amount, *args, **kwargs):
  print(get_access_token())
  access_token = get_access_token()
  print(access_token)
  if access_token:
    access_data = {
      'merchant_uid': merchant_id,
      'amount': amount
    }

    url = 'https://api.iamport.kr/payments/prepare'

    headers = {
      'Authorizetion': 'Baerer' + access_token
    }

    req = requests.post(url, data=access_data, headers=headers)
    res = req.json()

    if res['code'] is not 0:
      raise ValueError('API 연결에 문제가 생겼습니다.')
  else:
    raise ValueError('인증 토큰이 없습니다')

# 결제가 끝나고 나서 결제에 대한 정보를 가져오는 단계
def get_transaction(merchant_id, *args, **kwargs):
  access_token = get_access_token()

  if access_token:
    url = 'https://api.iamport.kr/payments/find/' + merchant_id

    headers = {
      'Authorization': access_token
    }
    
    req = requests.post(url, headers=headers)
    res = req.json()

    if res['code'] is 0:
      context = {
        'imp_id': res['response']['imp_uid'],
        'merchant_id': res['response']['merchant_uid'],
        'amount': res['response']['amount'],
        'status': res['response']['status'],
        'type': res['response']['pay_method'],
        'receipt_url': res['response']['receipt_url']
      }
      return context
    else:
      return None
  else:
    raise ValueError('인증 토큰이 없습니다.')
    