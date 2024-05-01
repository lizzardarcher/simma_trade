import sys
import traceback
import django
import os
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import asyncio
from pathlib import Path
import time
import json
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
django.setup()
from apps.main.models import *

log_path = Path(__file__).parent.absolute() / 'log.log'
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        # TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=5),
        # RotatingFileHandler(filename=log_path, maxBytes=10000, backupCount=5),
        logging.StreamHandler(stream=sys.stderr)
    ],
)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {SimaSettings.objects.get(pk=1).token}',
}


async def parse(start, stop, task_name):
    _ts = time.time()
    session = requests.Session()
    for i in range(start, stop):
        r2 = session.get(url=f'https://www.sima-land.ru/api/v3/category/?page={i}', headers=headers)
        logger.info(f'[{r2.url}]')
        if '422' in str(r2):
            logger.error(r2.text)
        data = r2.json()['items']
        for item in data:
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
    task_1 = asyncio.create_task(parse(start=1, stop=850, task_name=f'task_1'))
    background_tasks.add(task_1)
    task_1.add_done_callback(background_tasks.discard)


if __name__ == '__main__':
    ts = time.time()
    asyncio.run(main())
    te = time.time()
    logger.info(f'Total Finished in {te - ts:.2f} seconds')
