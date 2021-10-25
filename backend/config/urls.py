"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import (include, path)

# from allauth.views import ConfirmEmailView

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_url_patterns = [
    path('account/', include('sign.urls')),
    path('party/', include('party.urls')),
    path('billing/', include('billing.urls')),
    path('movies/', include('rec_movie.urls')),
    path('programs/', include('rec_program.urls')),
    ]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="BackEnd API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    # silk 적용
    path('silk/', include('silk.urls')),

    path('api/v1/admin/', admin.site.urls),
    path('api/v1/party/', include('party.urls')), # Party
    path('api/v1/account/', include('sign.urls')), # User
    path('api/v1/billing/', include('billing.urls')),
    path('api/v1/movies/', include('rec_movie.urls')),  # Movie contents
    path('api/v1/programs/', include('rec_program.urls')),  # Program contents

    # Swagger 연동
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
