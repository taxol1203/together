from django.contrib import admin
from .models import Genre, Movie, Provider, Review
# Register your models here.

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Provider)
admin.site.register(Review)

