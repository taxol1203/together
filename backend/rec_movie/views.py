import json
import pandas as pd
from django.http import (HttpResponse, Http404)
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile
import pickle

from .models import (Movie, Review, Genre, Provider)
from .serializers import (MovieSerializer, ReviewSerializer, GenreSerializer)

# recommend files
from .rec_py import (movie_rec_genre as rec_g, movie_rec_cbf as rec_m, movie_rec_top as rec_top)


# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def convert_movie_data(self):
    Movie.objects.all().delete()

    movie_id_set = set()    # 영화 데이터 중 movie_id를 저장할 set
    with open('./rec_movie/data/movies_kr.json', 'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)
    df = df.fillna(0)

    # json 형태의 영화를 하나씩 가져와서 확인한다.
    for idx, row in df.iterrows():
        # 중복된 영화가 등록 되는지 확인
        if row['pk'] in movie_id_set:
            continue
        movie_id_set.add(row['pk'])

        # release_date가 없는 영화가 1개 있다.
        if row['fields.release_date'] == '' or row['fields.release_date'] == 0 or row['fields.poster_path'] == 0:
            continue
        movie = Movie.objects.create(movie_id=row['pk'], original_title=row['fields.original_title'],
                                     title=row['fields.title'], overview=row['fields.overview'], release_date=row['fields.release_date'],
                                     poster_path=row['fields.poster_path'])
        # manyTomany로 연결 된 genre 데이터를 가져와서 연결한다.
        for genre_id in row['fields.genre_ids']:
            genre = Genre.objects.get(genre_id=genre_id)
            movie.genres.add(genre)

        # manyTomany로 연결 된 provider 데이터를 가져와서 연결한다.
        provider_set = set()
        if row['fields.provider.buy'] != 0:
            provider_list_to_set(provider_set, row['fields.provider.buy'])
        if row['fields.provider.rent'] != 0:
            provider_list_to_set(provider_set, row['fields.provider.rent'])
        if row['fields.provider.flatrate'] != 0:
            provider_list_to_set(provider_set, row['fields.provider.flatrate'])

        for provider_name in provider_set:
            try:
                provider = Provider.objects.get(name=provider_name)
                movie.providers.add(provider)
            except Provider.DoesNotExist:
                print(f"{provider_name}는 존재하지 않습니다.")

    return HttpResponse('Success convert json to database')


# row['fields.provider']에는 중복되는 provider가 있으므로, set을 통해 중복을 제거해준다.
def provider_list_to_set(p_set, p_list):
    size = len(p_list)
    for idx in range(0, size):
        p_set.add(p_list[idx]['provider_name'])


# tmdb의 reviews.json을 model로 변환하고 db에 넣는다.
def convert_review_data(request):
    Review.objects.all().delete()

    with open('./rec_movie/data/movie_reviews.json', 'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)
    for idx, row in df.iterrows():
        try:
            movie = Movie.objects.get(movie_id=row['movieId'])
        except Movie.DoesNotExist:
            print(f"{row['movieId']}는 존재하지 않습니다.")
        Review.objects.create(user_id=row['userId'], movie_id=movie, rating=row['rating'])

    return HttpResponse('Success convert json to database')


def convert_genre_data(self):
    Genre.objects.all().delete()

    with open('./rec_movie/data/movies_genre.json', 'r', encoding='UTF-8') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)

    for idx, row in df.iterrows():
        Genre.objects.create(genre_id=row['pk'], name=row['fields.name'], k_name=row['fields.k-name'])

    return HttpResponse('Success convert json to database')


# Review APIs
class ReviewView(GenericAPIView):
    queryset = Review.objects.all()  # Generic Api View는 반드시 포함 해야함
    serializer_class = ReviewSerializer

    def post(self, request, format=None):
        """
        리뷰를 등록하기 위한 API입니다.

        ---
        # Parameters
            - user_id : 유지 id(닉네임)
            - rating : 평가 점수 (0 ~ 10)
            - movie_id : 연계된 movie. movie의 primary key와 연결해야한다.

        responseMessages:
            - code: 201
              message: Success Create Album

        """
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object_review(self, pk):
        try:
            return Review.objects.get(id=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            review = self.get_object_review(pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        try:
            review = self.get_object_review(pk)
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk, format=None):
        review = self.get_object_review(pk)
        review.delete()
        try:
            return Response(status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@silk_profile(name='Get Movie data')
def get_movie(request, pk):
    """
    영화 정보를 가져옵니다.
    1. 영화의 정보
    2. 장르, 공급자
    3. 해당 영화와 관련있는 추천 영화들

    ---

    responseMessages:
        - code: 201
          message: Success Create Album

    """
    movie = get_object_or_404(Movie, id=pk)
    # 만약 추천된 영화가 없을 경우 수행한다.
    # 이것은 차후, 업데이트 할 시에, 현재 추천된 영화를 제거하고 새롭게 추천하는 과정으로 바꾸어야한다.
    if movie.recommends.count() == 0:
        # 현재 영화와 관련있는 추천 영화들을 연결한다.
        movie_ids = rec_m.recommend(movie.original_title)
        for movie_id in movie_ids:
            print(movie_id)
            rec_movie = get_object_or_404(Movie, movie_id=movie_id)
            movie.recommends.add(rec_movie)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
def get_genre(self):
    """
        모든 영화 장르를 가져옵니다.

        ---

        responseMessages:
            - code: 201
              message: Success Create Album

        """
    genre = Genre.objects.all()
    serializer = GenreSerializer(genre, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@silk_profile(name='Get Main data')
def get_genre_rec_movies(request):
    """
        메인 페이지에서 장르를 기준으로 가장 인기있는 영화를 추천해 줍니다.
        현재 임의로 3개의 장르를 설정하여 추천 알고리즘을 적용하였습니다.
        차후 User와 연결하여, User의 선호 장르를 읽어와 제공하도록 합니다.

        ---

        responseMessages:
            - code: 201
              message: Success Get Movies

        """
    # 로그인을 하지 않았을 때
    if request.user.username == '':
        movie_ids = rec_top.recommend()
    else:
        # 이후 유저의 정보를 받으면, 그 유저의 선호 장르 3개에 대한 추천 영화를 출력한다.
        genres = request.user.fav_movie_genres.all()
        genre_id = []
        for genre_name in genres:
            genre = Genre.objects.get(k_name=genre_name)
            # print(genre.genre_id)
            genre_id.append(genre.genre_id)
        # 사용자가 선호하는 장르가 3개 미만일 때
        if len(genre_id) < 3:
            movie_ids = rec_top.recommend()
        else:
            movie_ids = rec_g.recommend(genre_id[0], genre_id[1], genre_id[2])

    movies = []
    for movie_id in movie_ids:
        movie = get_object_or_404(Movie, movie_id=movie_id)
        movies.append(movie)

    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def testPickle(self):
    try:
        df = pickle.load(open("test.pickle", "rb"))
    except (OSError, IOError) as e:
        with open('./rec_movie/data/movies_kr.json', 'r') as f:
            data = json.loads(f.read())
        df = pd.json_normalize(data)
        pickle.dump(df, open("test.pickle", "wb"))
    result = 0
    for idx, row in df.iterrows():
        result = row['pk']
        break
    return HttpResponse(result)

