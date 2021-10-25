## Account



- package

```python
pip install dj-rest-auth # jwt account
pip install django-allauth # 소셜 로그인
pip install djangorestframework
```

- settings.py

```python
INSTALLED_APPS = [
    # --------------
    
    'drf_yasg',  # drf_yasg(swagger)
    # user authentioation basic module
    'django.contrib.sites',
    'allauth',
    'allauth.socialaccount', # 소셜 가입계정 관리
    'allauth.account',

    # provider
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',

    # app
    'sign.apps.SignConfig',
    
    # DRF
    'rest_framework',   
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
]
```

```python
# JWT, REST_AUTH Custom
# 디폴트 SITE의 id / 등록을 하지 않으면, 각 요청 시에 host명의 Site 인스턴스를 찾는다 .
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'sign.CustomUser'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False # 유저네임은 없어도 됨
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # 로그아웃 후 리디렉션 할 페이지
ACCOUNT_LOGOUT_ON_GET = True # 로그아웃 버튼 클릭 시 자동 로그아웃

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'sign.serializers.CustomUserDetailSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'sign.serializers.CustomRegisterSerializer',
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'


JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
}

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
}
```





### 유저관리

| 요청 URL                 | 메서드 | 설명          |
| ------------------------ | ------ | ------------- |
| /account/register        | POST   | 회원가입      |
| /account/login           | POST   | 로그인        |
| /account/logout          | GET    | 로그아웃      |
| /account/password/change | POST   | 비밀번호 변경 |
| /account/profile         | GET    | 프로필 확인   |
| /accounts/naver/login/   |        | 네이버 로그인 |
| /accounts/google/login/  |        | 구글 로그인   |

### `http://127.0.0.1:8000/swagger/` 에서 보다 쉽게 확인 가능



### 회원가입 [POST]

`http://127.0.0.1:8000/account/register/`

- Request

  - Body

  ```jso
  {
    "username": "string",
    "email": "user@example.com",
    "password1": "string",
    "password2": "string",
    "phone_number": "string",
    "nickname": "string"
  }
  ```

- Response

  - 201

  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMyNDg0NzE0LCJqdGkiOiJlMjA1MTk1NGVmZjY0ZDlmOGJiNjUzYzY0MDAzMzIwNCIsInVzZXJfaWQiOjZ9.C75tbG3oJgj4my0Uv5lDjcn2rxhZi8uSxO-z2LjlbA0",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjU3MDgxNCwianRpIjoiOTc2Y2RiNDRlOTFlNGJhMGE4OTNlNzFhMGMxYWQ1ZTAiLCJ1c2VyX2lkIjo2fQ.3EBy_391iPUnXNtfoWpFiw38Wq4lvNDiS4lSr-ynI-4",
    "user": {
      "pk": 6,
      "email": "user@example.com",
      "nickname": "string",
      "username": "string",
      "phone_number": "string"
    }
  }
  ```



### 로그인 [POST]

`http://127.0.0.1:8000/account/login/`

- Request

  - Body

  ```json
  {
    "username": "string", // 생략 가능
    "email": "user@example.com",
    "password": "string"
  }
  ```

- Response

  - 200

  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMyNDg0OTE2LCJqdGkiOiJjMzEyODIwMGMxNGY0MmY2OWJhZTg2OWI5ZDYyOWY2OSIsInVzZXJfaWQiOjF9.ADbrF5EtA5BmIetwhcgJIF6FHS8GJwgcyXEMKVNxIhg",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjU3MTAxNiwianRpIjoiOTQwNjE0OWExODE0NDc4MThhMzRjMDhlNzM2Yzk0YzMiLCJ1c2VyX2lkIjoxfQ.VOSHzWeWB_KpC1khrsjAtgPtCSvnlvdRluW4rm-SrpQ",
    "user": {
      "pk": 1,
      "email": "check@test.com",
      "nickname": "slrspdla",
      "username": "test",
      "phone_number": "010-0000-0000"
    }
  }
  ```

### 로그아웃 [GET]

`http://127.0.0.1:8000/account/logout/`

- Request

  - 없음

- Response

  - 200

  ```json
  {
    "detail": "로그아웃되었습니다."
  }
  ```

  

### 패스워드 변경[POST]

`http://127.0.0.1:8000/account/password/change/`

- Request

  - body

  ```json
  {
    "new_password1": "string",
    "new_password2": "string"
  }
  ```

- Response

  - 201

  ```json
  {
    "detail": "새로운 패스워드가 저장되었습니다."
  }
  ```



### 프로필[GET, PUT, PATCH]

`http://127.0.0.1:8000/account/profile/`

- GET 

  - Request : 없음

  - Response

    - 200

    ```json
    {
      "pk": 1,
      "email": "check@test.com",
      "nickname": "slrspdla",
      "username": "test",
      "phone_number": "010-0000-0000"
    }
    ```

- PUT

  - Request

    - Body

    ```json
    {
      "nickname": "string",
      "phone_number": "string"
    }
    ```

  - Response

    - 200

    ```json
    {
      "pk": 1,
      "email": "check@test.com",
      "nickname": "string",
      "username": "test",
      "phone_number": "string"
    }
    ```

- PATCH 생략..

