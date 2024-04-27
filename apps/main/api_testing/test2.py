import sys
import traceback
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from pathlib import Path

import django
import os
import logging
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")

django.setup()
from apps.main.models import *

import asyncio
import time
import json
import requests


log_path = Path(__file__).parent.absolute() / 'log.log'
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        # TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=5),
        RotatingFileHandler(filename=log_path, maxBytes=10000, backupCount=5),
        logging.StreamHandler(stream=sys.stderr)
    ],
)


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTMxNzA4NDQsIm5iZiI6MTcxMzE3MDg0NCwiZXhwIjoxNzQ0NzA2ODQ0LCJqdGkiOjY1NjI1MTB9.Fc2FYDKEpcIW8sc6V5ccY5su81BE61L6DGtpWUwdjTs'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
}

# json = {
#     'id': None,
#     'level': 1,
#     'path': None,
#     'is_not_empty': 1,
#     'with_adult': 1,
#     'is_adult': None,
#     'expand-root': 1,
#     'full_slug': None,
#     'id-greater-than': None,
#     'is_active': None,
#     'is_for_mobile_app': None,
#     'type': 0,
# }
# r = requests.get(url='GET https://www.sima-land.ru/api/v3/item/')
# r1 = requests.get(url='https://www.sima-land.ru/api/v3/category/', headers=headers)
# items = r1.json()['items']
# cat_ids = [item['id'] for item in items]
# print(r1)
# print(cat_ids)

# json = {
#     # 'category_id': cat_ids.__str__().replace(']', '').replace('[', ''),
#     'category_id': '1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19',
#     'has_price': 1,
#     'has_balance': 1,
# }
# '19769'
from functools import wraps


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        ts = time.time()
        result = fn(*args, **kwargs)
        te = time.time()
        print(f'Function {fn.__name__} took {te - ts}')
        return result

    return measure_time


async def parse(start, stop, task_name):
    _ts = time.time()
    for i in range(start, stop):
        r2 = requests.get(url=f'https://www.sima-land.ru/api/v3/category/?expand=description&page={i}', headers=headers)
        if '422' in str(r2):
            logger.error(r2.text)
        data = r2.json()['items']
        # logger.info(len(data))
        for item in data:
            logger.info(item)
            try:
                await SimaCategory.objects.aupdate_or_create(
                    defaults={'name': item['name'],
                              'sid': item['sid']
                              },
                    cat_id=item['id'],
                )
            except asyncio.CancelledError as e:
                logger.error(e)
    _te = time.time()
    logger.info(f"{task_name} finished in {_ts - _te} seconds")


async def main():
    background_tasks = set()
    task_1 = asyncio.create_task(parse(start=1, stop=2000, task_name=f'task_1'))
    background_tasks.add(task_1)
    task_1.add_done_callback(background_tasks.discard)


if __name__ == '__main__':
    ts = time.time()
    asyncio.run(main())
    te = time.time()
    logger.info(f'Total Finished in {te - ts:.2f} seconds')
