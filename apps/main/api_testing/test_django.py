import django
import os
import logging
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")

django.setup()
from apps.main.models import *

cat_ids = [x.cat_id for x in SimaCategory.objects.all()]
print(cat_ids.__len__())