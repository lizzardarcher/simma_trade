import ast
import math
import sys
import traceback
import xml
import os
import asyncio
import logging
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
import json
import re
import requests

import aiohttp  # pip install aiohttp aiodns
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'sima_trade.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.main.models import *

log_path = Path(__file__).parent.absolute() / 'log_parser.log'
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.WARNING,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        # TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=5),
        RotatingFileHandler(filename=log_path, maxBytes=100000, backupCount=5),
        # logging.StreamHandler(stream=sys.stderr)
    ],
)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {SimaSettings.objects.get(pk=1).token}',
}

cat_ids = [x.cat_id for x in SimaCategory.objects.all()]
empty_cat = []
CLEANR = re.compile('<.*?>')


def get_pairs(max_id, threads):
    data = []
    counter = 1
    l_ids = [x for x in range(1, max_id + 1)]
    chunk_size = math.floor(max_id / threads)
    chunks = [l_ids[i:i + chunk_size] for i in range(0, len(l_ids), chunk_size)]
    for chunk in chunks:
        data.append((f'thread-{counter}', chunk[0], chunk[-1]))
        counter += 1
    print(data)
    return data


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


async def get(session: aiohttp.ClientSession, color: str, **kwargs) -> dict:
    url = f"https://api.com/{color}/"
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)
    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    data = await resp.json()
    print(f"Received data for {url}")
    return data


async def parse(session: aiohttp.ClientSession, start, stop, task_name, **kwargs):
    ts = time.time()
    per_page = 100
    for i in range(start, stop):
        if i in cat_ids:

            try:
                resp = await session.request(method='GET',
                                             url=f'https://www.sima-land.ru/api/v3/item/?per-page={per_page}&category_id={i}&'
                                                 f'is_remote_store=0&expand=files,categories,all_categories,description,stocks,attrs',
                                             headers=headers, **kwargs)

                data = await resp.text()
                data_items = json.loads(data)['items']

                if len(data_items) > 0:
                    pages = json.loads(data)['_meta']['pageCount']
                    try:
                        if pages > 1:
                            for page in range(pages + 1):
                                if page > 1:
                                    per_page_resp = await session.request(
                                        method='GET',
                                        url=f'https://www.sima-land.ru/api/v3/item/?per-page={per_page}&category_id={i}&page='
                                            f'{page}&is_remote_store=0&expand=files,categories,all_categories,description,stocks,attrs',
                                        headers=headers, **kwargs)
                                    per_page_data = await per_page_resp.text()
                                    per_page_data = json.loads(per_page_data)['items']
                                    for item in per_page_data:
                                        if item['price'] < 7000:

                                            stock = 0
                                            stocks = ast.literal_eval(str(item['stocks']))
                                            for s in stocks:
                                                try:
                                                    if s['balance_text']:
                                                        stock += 50
                                                    else:
                                                        stock += s['balance']
                                                except KeyError:
                                                    pass
                                            trademark = ''
                                            try:
                                                trademark = item['trademark']['name']
                                            except:
                                                pass
                                            desc = cleanhtml(item['description'])
                                            await SimaItem.objects.aupdate_or_create(defaults={
                                                "item_id": item['id'],
                                                "sid": item['sid'],
                                                "name": item['name'],
                                                "minimum_order_quantity": item['minimum_order_quantity'],
                                                "price": item['price'],
                                                "price_max": item['price_max'],
                                                "currency": item['currency'],
                                                "boxtype_id": item['boxtype_id'],
                                                "box_depth": item['box_depth'],
                                                "box_height": item['box_height'],
                                                "box_width": item['box_width'],
                                                "in_box": item['in_box'],
                                                "in_set": item['in_set'],
                                                "depth": item['depth'],
                                                "unit_id": item['unit_id'],
                                                "width": item['width'],
                                                "height": item['height'],
                                                "max_qty": item['max_qty'],
                                                "min_qty": item['min_qty'],
                                                "package_volume": item['package_volume'],
                                                "product_volume": item['product_volume'],
                                                "box_volume": item['box_volume'],
                                                "box_capacity": item['box_capacity'],
                                                "photo_url": item['photoUrl'],
                                                "vat": item['vat'],
                                                "supplier_code": item['supplier_code'],
                                                "weight": item['weight'],
                                                "img": item['img'],
                                                "size": item['size'],
                                                "stuff": item['stuff'],
                                                "trademark": trademark,
                                                "categories": item['categories'],
                                                "description": desc,
                                                "stocks": stock,
                                                "attrs": item['attrs'],
                                            }, item_id=item['id'])
                                    logger.info(
                                        f'[{task_name}] [{str(per_page_resp.url).split("expand")[0]}] [items: {len(data_items)}] ')
                    except:
                        logger.error(traceback.format_exc().__str__())

                    logger.info(
                        f'[{task_name}] [{str(resp.url).split("expand")[0]}] [items: {len(data_items)}] [pages: {str(pages)}]')

                    for item in data_items:
                        if item['price'] < 7000:
                            try:
                                stock = 0
                                stocks = ast.literal_eval(str(item['stocks']))
                                for s in stocks:
                                    try:
                                        if s['balance_text']:
                                            stock += 50
                                        else:
                                            stock += s['balance']
                                    except KeyError:
                                        pass

                                trademark = ''
                                try:
                                    trademark = item['trademark']['name']
                                except:
                                    pass
                                desc = cleanhtml(item['description'])

                                await SimaItem.objects.aupdate_or_create(defaults={
                                        "item_id": item['id'],
                                        "sid": item['sid'],
                                        "name": item['name'],
                                        "minimum_order_quantity": item['minimum_order_quantity'],
                                        "price": item['price'],
                                        "price_max": item['price_max'],
                                        "currency": item['currency'],
                                        "boxtype_id": item['boxtype_id'],
                                        "box_depth": item['box_depth'],
                                        "box_height": item['box_height'],
                                        "box_width": item['box_width'],
                                        "in_box": item['in_box'],
                                        "in_set": item['in_set'],
                                        "depth": item['depth'],
                                        "unit_id": item['unit_id'],
                                        "width": item['width'],
                                        "height": item['height'],
                                        "max_qty": item['max_qty'],
                                        "min_qty": item['min_qty'],
                                        "package_volume": item['package_volume'],
                                        "product_volume": item['product_volume'],
                                        "box_volume": item['box_volume'],
                                        "box_capacity": item['box_capacity'],
                                        "photo_url": item['photoUrl'],
                                        "vat": item['vat'],
                                        "supplier_code": item['supplier_code'],
                                        "weight": item['weight'],
                                        "img": item['img'],
                                        "size": item['size'],
                                        "stuff": item['stuff'],
                                        "trademark": trademark,
                                        "categories": item['categories'],
                                        "description": desc,
                                        "stocks": stock,
                                        "attrs": item['attrs'],
                                    }, item_id=item['id'])

                            except asyncio.CancelledError as e:
                                logger.error(e)
                else:
                    pass
            except:
                logger.error(traceback.format_exc().__str__())
        await asyncio.sleep(1)
    te = time.time()
    logger.warning(
        f"[{task_name}] [ cat: {str(start)} - {str(stop)}] [finished in {str(float((ts - te) / 60))} minutes]")


async def main():
    try:
        await asyncio.sleep(5)
        # logger.info(f"Dropping Table Started")
        # await SimaItem.objects.filter(item_id__gte=0).adelete()
        # logger.info(f"Dropping Table Finished")

        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in get_pairs(max_id=77000, threads=64):
                tasks.append(parse(session=session, start=i[1], stop=i[2], task_name=i[0]))
            htmls = await asyncio.gather(*tasks, return_exceptions=True)
            return htmls
    except:
        logger.error(traceback.format_exc().__str__())


if __name__ == '__main__':
    ts = time.time()
    asyncio.run(main())
    te = time.time()
    logger.warning(f'[Total Finished in {str(float((te - ts) / 60))} minutes]')
