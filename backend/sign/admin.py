from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm,UserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
  form = UserChangeForm
  add_form = UserCreationForm

  list_display = ('email', 'nick_name', 'phone_number', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
    ('Email & Password',
      {'fields':
        ('email','password')
      }
    ),
    ("Personal info",
      {'fields':
        ('nick_name','phone_number')
      }
    ),
    ("Permissions",
      {'fields':
        ('is_admin',)
      }
    ),
    ("FavGenres",
      {'fields':
        ('fav_movie_genres', 'fav_program_genres')
      }
    ),
  )
  add_fieldsets = (
    (None, {
      'classes':('wide',),
      'fields': ('email', 'nick_name', 'phone_number', 'password1', 'password2')
    }),
  )
  search_fields = ('email',)
  ordering = ('email',)
  filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
