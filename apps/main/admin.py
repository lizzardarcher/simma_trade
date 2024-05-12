from django.contrib import admin
from apps.main.models import *

admin.site.site_title = 'Sima Trade'
admin.site.site_header = 'Sima Trade Administararion'
admin.site.index_title = 'Sima Trade Administararion'
admin.site.site_url = ''


# Register your models here.

@admin.register(SimaItem)
class SimaItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_id', 'stocks')
    # search_fields = ('sid',)
    search_fields = ('name', 'item_id', 'sid')
    # search_fields = ('attrs',)
    search_help_text = 'Введите артикул, id или название товара'
    show_full_result_count = False
    ordering = ('item_id',)


@admin.register(SimaCategory)
class SimaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'cat_id')
    search_fields = ('name', 'cat_id')
    ordering = ('name',)
    show_full_result_count = False


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('-id',)


@admin.register(SimaFilter)
class SimaFilterAdmin(admin.ModelAdmin):
    fields = ('filter_id',
              'max_price',
              'min_stock',
              ('max_width',
               'min_width'),
              ('max_height',
               'min_height'),
              ('max_depth',
               'min_depth'),
              )


@admin.register(SimaSettings)
class SimaSettingsAdmin(admin.ModelAdmin):
    ...


@admin.register(SimaBlacklist)
class SimaBlacklistAdmin(admin.ModelAdmin):
    ...


@admin.register(XMLFeed)
class XMLFeedAdmin(admin.ModelAdmin):
    ...


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    ...


@admin.register(MarketPlace)
class MarketPlaceAdmin(admin.ModelAdmin):
    ...