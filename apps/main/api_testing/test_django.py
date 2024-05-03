import django
import os
import logging
import ast
from collections import defaultdict
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
django.setup()
from apps.main.models import *

# cat_ids = [x.cat_id for x in SimaCategory.objects.all()]
# print(cat_ids.__len__())
'''
<item>
<id>5511</id>
<settlement_id>415271112</settlement_id>
<address>620920, Свердловская обл, Екатеринбург г, Северка п - Получение заказа с машины</address>
</item>
'''
item = SimaItem.objects.all().first()

print(item.stocks, type(item.stocks))
stocks = ast.literal_eval(item.stocks)
print(stocks, type(stocks))
