from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Movie(models.Model):
    movie_id = models.CharField(max_length=10, default='', unique=True)
    original_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100, default='')
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=40)    # https://image.tmdb.org/t/p/original/[poster_path]
    genres = models.ManyToManyField('Genre')        # many to many로 genre와 연결하였다. related_name은 자동으로 'genres'
    providers = models.ManyToManyField('Provider')  # many to many로 provider와 연결하였다. related_name은 자동으로 'provider'
    # 자기 참조 외래키로, 추천 영화를 해당 영화 내부에 기입한다.
    # https://himanmengit.github.io/django/2018/02/06/DjangoModels-07-ManyToMany-Self-Symmetrical.html
    recommends = models.ManyToManyField('self', symmetrical=False, blank=True)


class Genre(models.Model):
    genre_id = models.IntegerField()
    name = models.CharField(max_length=20)
    k_name = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.k_name


class Review(models.Model):
    user_id = models.CharField(max_length=100)
    movie_id = models.ForeignKey("Movie", related_name="reviews", on_delete=models.CASCADE, db_column="movie_id")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie_id.title}: {self.user_id}의 리뷰"


class Provider(models.Model):
    name = models.CharField(max_length=20)
    pricePerDay = models.IntegerField(default=0)
    logo_url = models.CharField(max_length=100, default='')
