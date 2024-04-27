import math
import sys
import traceback

import django
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'sima_trade.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from apps.main.models import *
import asyncio
import logging
import time
from pathlib import Path
import json
import aiohttp  # pip install aiohttp aiodns
import requests

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

# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTMxNzA4NDQsIm5iZiI6MTcxMzE3MDg0NCwiZXhwIjoxNzQ0NzA2ODQ0LCJqdGkiOjY1NjI1MTB9.Fc2FYDKEpcIW8sc6V5ccY5su81BE61L6DGtpWUwdjTs'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {SimaSettings.objects.get(pk=1).token}',
}

cat_ids = [x.cat_id for x in SimaCategory.objects.all()]
empty_cat = []
with open('empty_cat.txt', 'r') as f:
    cat = f.readline().replace('\n', '')
    empty_cat.append(int(cat))


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


async def get(
        session: aiohttp.ClientSession,
        color: str,
        **kwargs
) -> dict:
    url = f"https://api.com/{color}/"
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)
    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    data = await resp.json()
    print(f"Received data for {url}")
    return data


async def parse(session: aiohttp.ClientSession, start, stop, task_name, **kwargs):
    per_page = 100
    _ts = time.time()
    for i in range(start, stop):
        if i in cat_ids and i not in empty_cat:

            try:
                resp = await session.request(method='GET',
                                             url=f'https://www.sima-land.ru/api/v3/item/?per-page={per_page}&category_id={i}&'
                                                 f'is_remote_store=0&expand=materials,authors,notices,files,'
                                                 f'categories,all_categories,modifier_items,description,ext_description,'
                                                 f'extra_notices,stocks,attrs',
                                             headers=headers, **kwargs)

                data = await resp.text()
                data_items = json.loads(data)['items']

                if len(data_items) > 0:
                    pages = json.loads(data)['_meta']['pageCount']
                    try:
                        # pages = json.loads(data)['_meta']['pageCount']
                        if pages > 1:
                            for page in range(pages + 1):
                                if page > 1:
                                    per_page_resp = await session.request(
                                        method='GET',
                                        url=f'https://www.sima-land.ru/api/v3/item/?per-page={per_page}&category_id={i}&page='
                                            f'{page}&is_remote_store=0&expand=materials,authors,notices,files,'
                                            f'categories,all_categories,modifier_items,description,ext_description,'
                                            f'extra_notices,stocks,attrs',
                                        headers=headers, **kwargs)
                                    per_page_data = await per_page_resp.text()
                                    per_page_data = json.loads(per_page_data)['items']
                                    # data_items += per_page_data
                                    for item in per_page_data:
                                        if item['price'] < 7000:
                                            await SimaItem.objects.aupdate_or_create(defaults={
                                                "item_id": item['id'],
                                                "sid": item['sid'],
                                                "uid": item['uid'],
                                                "name": item['name'],
                                                "slug": item['slug'],
                                                "is_disabled": item['is_disabled'],
                                                "reason_of_disabling": item['reason_of_disabling'],
                                                "minimum_order_quantity": item['minimum_order_quantity'],
                                                "price": item['price'],
                                                "price_max": item['price_max'],
                                                "price_per_square_meter": item['price_per_square_meter'],
                                                "price_per_linear_meter": item['price_per_linear_meter'],
                                                "currency": item['currency'],
                                                "created_at": item['created_at'],
                                                "updated_at": item['updated_at'],
                                                "boxtype_id": item['boxtype_id'],
                                                "box_depth": item['box_depth'],
                                                "box_height": item['box_height'],
                                                "box_width": item['box_width'],
                                                "in_box": item['in_box'],
                                                "in_set": item['in_set'],
                                                "depth": item['depth'],
                                                "unit_id": item['unit_id'],
                                                "nested_unit_id": item['nested_unit_id'],
                                                "width": item['width'],
                                                "height": item['height'],
                                                "trademark_id": item['trademark_id'],
                                                "country_id": item['country_id'],
                                                "cart_min_diff": item['cart_min_diff'],
                                                "keep_package": item['keep_package'],
                                                "per_package": item['per_package'],
                                                "page_title": item['page_title'],
                                                "page_keywords": item['page_keywords'],
                                                "page_description": item['page_description'],
                                                "parent_item_id": item['parent_item_id'],
                                                "max_qty": item['max_qty'],
                                                "min_qty": item['min_qty'],
                                                "modifier_id": item['modifier_id'],
                                                "modifier_value": item['modifier_value'],
                                                "qty_multiplier": item['qty_multiplier'],
                                                "surface_area": item['surface_area'],
                                                "linear_meters": item['linear_meters'],
                                                "package_volume": item['package_volume'],
                                                "min_age": item['min_age'],
                                                "power": item['power'],
                                                "volume": item['volume'],
                                                "is_boxed": item['is_boxed'],
                                                "product_volume": item['product_volume'],
                                                "box_volume": item['box_volume'],
                                                "box_capacity": item['box_capacity'],
                                                "packing_volume_factor": item['packing_volume_factor'],
                                                "isbn": item['isbn'],
                                                "page_count": item['page_count'],
                                                "is_add_to_cart_multiple": item['isAddToCartMultiple'],
                                                "supply_period": item['supply_period'],
                                                "photo_url": item['photoUrl'],
                                                "type": item['type'],
                                                "vat": item['vat'],
                                                "currency_sign": item['currencySign'],
                                                "is_enough": item['isEnough'],
                                                "supplier_code": item['supplier_code'],
                                                "weight": item['weight'],
                                                "min_sum_order": item['min_sum_order'],
                                                "is_remote_store": item['is_remote_store'],
                                                "color": item['color'],
                                                "image_title": item['image_title'],
                                                "image_alt": item['image_alt'],
                                                "short_name": item['short_name'],
                                                "min_sum_for_free_delivery": item['min_sum_for_free_delivery'],
                                                "updated_item_at": item['updated_item_at'],
                                                "img": item['img'],
                                                "real_min_qty": item['real_min_qty'],
                                                "item_url": item['itemUrl'],
                                                "price_unit": item['price_unit'],
                                                "modifiers_count": item['modifiers_count'],
                                                "size": item['size'],
                                                "stuff": item['stuff'],
                                                "trademark": item['trademark'],
                                                "series": item['series'],
                                                "materials": item['materials'],
                                                "authors": item['authors'],
                                                "notices": item['notices'],
                                                "files": item['files'],
                                                "categories": item['categories'],
                                                "all_categories": item['all_categories'],
                                                "modifier_items": item['modifier_items'],
                                                "description": item['description'],
                                                "ext_description": item['ext_description'],
                                                "extra_notices": item['extra_notices'],
                                                "stocks": item['stocks'],
                                                "attrs": item['attrs'],
                                            }, item_id=item['id'])
                                    logger.info(f'[{task_name}] [{str(per_page_resp.url).split("expand")[0]}] [items: {len(data_items)}] ')
                    except:
                        logger.error(traceback.format_exc().__str__())

                    logger.info(f'[{task_name}] [{str(resp.url).split("expand")[0]}] [items: {len(data_items)}] [pages: {str(pages)}]')

                    for item in data_items:
                        # logger.info(item['id'])
                        try:
                            if item['price'] < 7000:
                                await SimaItem.objects.aupdate_or_create(defaults={
                                    "item_id": item['id'],
                                    "sid": item['sid'],
                                    "uid": item['uid'],
                                    "name": item['name'],
                                    "slug": item['slug'],
                                    "is_disabled": item['is_disabled'],
                                    "reason_of_disabling": item['reason_of_disabling'],
                                    "minimum_order_quantity": item['minimum_order_quantity'],
                                    "price": item['price'],
                                    "price_max": item['price_max'],
                                    "price_per_square_meter": item['price_per_square_meter'],
                                    "price_per_linear_meter": item['price_per_linear_meter'],
                                    "currency": item['currency'],
                                    "created_at": item['created_at'],
                                    "updated_at": item['updated_at'],
                                    "boxtype_id": item['boxtype_id'],
                                    "box_depth": item['box_depth'],
                                    "box_height": item['box_height'],
                                    "box_width": item['box_width'],
                                    "in_box": item['in_box'],
                                    "in_set": item['in_set'],
                                    "depth": item['depth'],
                                    "unit_id": item['unit_id'],
                                    "nested_unit_id": item['nested_unit_id'],
                                    "width": item['width'],
                                    "height": item['height'],
                                    "trademark_id": item['trademark_id'],
                                    "country_id": item['country_id'],
                                    "cart_min_diff": item['cart_min_diff'],
                                    "keep_package": item['keep_package'],
                                    "per_package": item['per_package'],
                                    "page_title": item['page_title'],
                                    "page_keywords": item['page_keywords'],
                                    "page_description": item['page_description'],
                                    "parent_item_id": item['parent_item_id'],
                                    "max_qty": item['max_qty'],
                                    "min_qty": item['min_qty'],
                                    "modifier_id": item['modifier_id'],
                                    "modifier_value": item['modifier_value'],
                                    "qty_multiplier": item['qty_multiplier'],
                                    "surface_area": item['surface_area'],
                                    "linear_meters": item['linear_meters'],
                                    "package_volume": item['package_volume'],
                                    "min_age": item['min_age'],
                                    "power": item['power'],
                                    "volume": item['volume'],
                                    "is_boxed": item['is_boxed'],
                                    "product_volume": item['product_volume'],
                                    "box_volume": item['box_volume'],
                                    "box_capacity": item['box_capacity'],
                                    "packing_volume_factor": item['packing_volume_factor'],
                                    "isbn": item['isbn'],
                                    "page_count": item['page_count'],
                                    "is_add_to_cart_multiple": item['isAddToCartMultiple'],
                                    "supply_period": item['supply_period'],
                                    "photo_url": item['photoUrl'],
                                    "type": item['type'],
                                    "vat": item['vat'],
                                    "currency_sign": item['currencySign'],
                                    "is_enough": item['isEnough'],
                                    "supplier_code": item['supplier_code'],
                                    "weight": item['weight'],
                                    "min_sum_order": item['min_sum_order'],
                                    "is_remote_store": item['is_remote_store'],
                                    "color": item['color'],
                                    "image_title": item['image_title'],
                                    "image_alt": item['image_alt'],
                                    "short_name": item['short_name'],
                                    "min_sum_for_free_delivery": item['min_sum_for_free_delivery'],
                                    "updated_item_at": item['updated_item_at'],
                                    "img": item['img'],
                                    "real_min_qty": item['real_min_qty'],
                                    "item_url": item['itemUrl'],
                                    "price_unit": item['price_unit'],
                                    "modifiers_count": item['modifiers_count'],
                                    "size": item['size'],
                                    "stuff": item['stuff'],
                                    "trademark": item['trademark'],
                                    "series": item['series'],
                                    "materials": item['materials'],
                                    "authors": item['authors'],
                                    "notices": item['notices'],
                                    "files": item['files'],
                                    "categories": item['categories'],
                                    "all_categories": item['all_categories'],
                                    "modifier_items": item['modifier_items'],
                                    "description": item['description'],
                                    "ext_description": item['ext_description'],
                                    "extra_notices": item['extra_notices'],
                                    "stocks": item['stocks'],
                                    "attrs": item['attrs'],
                                }, item_id=item['id'])

                        except asyncio.CancelledError as e:
                            # print(item)
                            logger.error(e)
                else:
                    with open('empty_cat.txt', 'a') as f:
                        f.write(f"{i}\n")
            except:
                logger.error(traceback.format_exc().__str__())
        await asyncio.sleep(1)
    _te = time.time()
    logger.info(f"{task_name} finished in {_ts - _te} seconds")


async def main():
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in get_pairs(max_id=80000, threads=16):
                tasks.append(parse(session=session, start=i[1], stop=i[2], task_name=i[0]))
            # asyncio.gather() will wait on the entire task set to be
            # completed.  If you want to process results greedily as they come in,
            # loop over asyncio.as_completed()
            htmls = await asyncio.gather(*tasks, return_exceptions=True)
            return htmls
    except:
        logger.error(traceback.format_exc().__str__())


if __name__ == '__main__':
    # Either take colors from stdin or make some default here
    asyncio.run(main())  # Python 3.7+
