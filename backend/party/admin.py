from django.contrib import admin
from .models import Party, Provider

class PartyAdmin(admin.ModelAdmin):
    list_display = ('title', 'member_limit', 'end_date', 'price_per_day')

class ProviderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Party, PartyAdmin)
admin.site.register(Provider, ProviderAdmin)