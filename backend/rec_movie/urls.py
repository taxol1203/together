from django.urls import path, include
from . import views

app_name = 'movieApp'    # URL 네임스페이스

urlpatterns = [
    path('convert-movie/', views.convert_movie_data),
    path('convert-review/', views.convert_review_data),
    path('convert-genre/', views.convert_genre_data),

    # movie
    path('<int:pk>/', views.get_movie),
    path('', views.get_genre_rec_movies),

    # review
    path('review/', views.ReviewView.as_view()),
    path('review/<int:pk>/', views.ReviewDetailView.as_view()),

    # genre
    path('genre/', views.get_genre),

    # test
    path('test/', views.testPickle),
]
