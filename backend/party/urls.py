from django.urls import path
from . import views

urlpatterns = [
  path('', views.PartyView.as_view()),
  path('<int:party_idx>/', views.PartyDetailView.as_view()),
  path('<int:party_idx>/payments/', views.PartyJoinView.as_view()),
  path('providers/', views.ProviderView.as_view()),
]