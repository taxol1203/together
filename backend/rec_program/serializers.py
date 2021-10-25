from rest_framework import serializers  # serializer import
from .models import Program, Review, Genre, Provider


class ReviewSerializerP(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class GenreSerializerP(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ProviderSerializerP(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class SubProgramSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField('get_genres')
    providers = ProviderSerializerP(read_only=True, many=True)
    class Meta:
        model = Program
        fields = '__all__'

    def get_genres(self, program):
        res = []
        genres = program.genres.all()
        for genre in genres:
            res.append(genre.k_name)
        return res


class ProgramSerializer(serializers.ModelSerializer):
    # genres = GenreSerializerP(read_only=True, many=True)
    genres = serializers.SerializerMethodField('get_genres')
    providers = ProviderSerializerP(read_only=True, many=True)
    recommends = SubProgramSerializer(read_only=True, many=True)
    reviews = serializers.SerializerMethodField('get_reviews')

    class Meta:
        model = Program
        fields = '__all__'
        read_only_fields = ('genres', 'providers', 'recommends')      # 장르 데이터도 함께 json으로 변환하여 제공한다.

    def get_genres(self, movie):
        res = []
        genres = movie.genres.all()
        for genre in genres:
            res.append(genre.k_name)
        return res


    def get_reviews(self, movie):
        reviews = movie.reviews.all().order_by('-created_at')
        return ReviewSerializerP(reviews, many=True).data