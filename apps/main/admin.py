from django.contrib import admin
from apps.main.models import *

admin.site.site_title = 'Sima Trade'
admin.site.site_header = 'Sima Trade Administararion'
admin.site.index_title = 'Sima Trade Administararion'
admin.site.site_url = ''
# Register your models here.
@admin.register(SimaItem)
class SimaItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
