from django.conf.urls import url
from django.contrib import admin
from .views import (
    charge_point,
    PointCheckoutAjaxView,
    PointImpAjaxView,
)
app_name= 'billing'

urlpatterns = [
    url('charge/', charge_point),
    url('checkout/', PointCheckoutAjaxView.as_view(), name='point_checkout'),
    url('validation/', PointImpAjaxView.as_view(), name='point_validation'),
]