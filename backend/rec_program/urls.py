from django.urls import path, include
from . import views

app_name = 'programApp'    # URL 네임스페이스

urlpatterns = [
    path('convert-program/', views.convert_program_data),
    path('convert-genre/', views.convert_genre_data),
    path('convert-review/', views.convert_review_data),
    path('genre-test/', views.find_not_exist_genre),

    # program
    path('<int:pk>/', views.get_program),
    path('', views.get_genre_rec_programs),

    # review
    path('review/', views.ReviewView.as_view()),
    path('review/<int:pk>/', views.ReviewDetailView.as_view()),

    # genre
    path('genre/', views.get_genre),
]
