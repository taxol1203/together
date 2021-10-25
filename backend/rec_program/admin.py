from django.contrib import admin
from .models import Genre, Program, Provider, Review

# Register your models here.
admin.site.register(Genre)
admin.site.register(Program)
admin.site.register(Provider)
admin.site.register(Review)