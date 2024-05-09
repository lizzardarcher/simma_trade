import math
import sys
import time
import asyncio
from logging.handlers import RotatingFileHandler

import django
import os
import ast
from pathlib import Path
import logging
import re
from datetime import datetime
import xml.etree.ElementTree as ET

from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
django.setup()
from apps.main.models import *
from apps.main.parser import prices

os.environ["PYTHONMAXSIZE"] = "3221225472"
local_time = datetime.now().strftime('%Y-%m-%dT%H:%M+05:00')
log_path = Path(__file__).parent.absolute() / 'log_xml.log'
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


async def create_xml(max_count, file_count):
    pairs = []
    l_ids = [x for x in range(1, max_count + 1)]
    chunk_size = math.floor(max_count / file_count)
    chunks = [l_ids[i:i + chunk_size] for i in range(0, len(l_ids), chunk_size)]
    for chunk in chunks:
        pairs.append((chunk[0], chunk[-1]))
    counter = 1
    logger.info(pairs)
    for pair in pairs:

        file = f'offers{str(counter)}.xml'
        path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("static").joinpath("media") / file
        root = ET.Element("yml_catalog", attrib={"date": f"{local_time}"})
        shop = ET.SubElement(root, "shop")

        ts = time.time()
        categories = ET.SubElement(shop, "categories")

        #  Начало Создания категорий
        cts = set()
        logger.info(f'File: {file} Creating categories...')
        items = SimaItem.objects.all().order_by('item_id')[pair[0]:pair[1]]
        for item in iter(items):
            # print('Категории', sorted(ast.literal_eval(item.categories)), type(ast.literal_eval(item.categories)))
            for i in sorted(ast.literal_eval(item.categories)):
                # if not i.startswith('7'):
                cts.add(i)
            # cts.add(sorted(ast.literal_eval(item.categories))[0])
            # await asyncio.sleep(5)
        # print('Длина списка категорий', len(cts))
        logger.info('Adding categories to XML ...')
        for cat_id in cts:
             # "parentId": "3798"
            try:
                ET.SubElement(categories, "category", attrib={"id": f"{str(cat_id)}"}).text = f"{SimaCategory.objects.get(cat_id=cat_id).name}"
            except:
                ET.SubElement(categories, "category", attrib={"id": f"{str(cat_id)}"})
        #  Создание категорий Закончено
        te = time.time()
        logger.info(f'Creating categories finished in {te - ts:.2f} seconds')

        shipment_options = ET.SubElement(shop, "shipment-options")
        option = ET.SubElement(shipment_options, "option", attrib={"days": "1", "order-before": "15"})
        offers = ET.SubElement(shop, "offers")

        ts = time.time()
        logger.info('Creating items...')

        # print('Длина списка товаров', items.count())

        for item in iter(items):
            offer = ET.SubElement(offers, "offer", attrib={"id": f"{str(item.item_id)}", "available": "true"})

            # ET.SubElement(offer, "url").text = "http://www.abc.ru/158.html"

            item_name = item.name
            if item.min_qty > 1:
                item_name = f"{item_name} ({str(item.min_qty)} шт.)"
            ET.SubElement(offer, "name").text = f"{item_name}"

            # print('Название товара:', item.name)
            item_price = float(item.price) * item.min_qty
            # print('item_price', item.price, '*', item.min_qty, '=', item_price)
            item_price_max = float(item.price_max) * item.min_qty
            # print('item_price_max', item.price, '*', item.min_qty, '=', item_price)

            for p in prices.price_ratio:
                if float(item_price) <= p[0]:
                    # print('price match with values', p[0], p[1], item_price)
                    item_price = float(item_price) * p[1]
                    # print('item_price after', item_price)
                    item_price_max = float(item_price_max) * p[1]
                    # print('item_price_max after', item_price)
                    break
            # await asyncio.sleep(10)

            ET.SubElement(offer, "price").text = f"{str(item_price)}"
            ET.SubElement(offer, "oldprice").text = f"{str(item_price_max)}"

            ET.SubElement(offer, "categoryId").text = f"{sorted(ast.literal_eval(item.categories))[0]}"
            ET.SubElement(offer, "picture").text = f"{item.photo_url}"

            item_vat = 0
            if int(item.vat) == 20:
                item_vat = 1
            elif int(item.vat) == 10:
                item_vat = 2
            ET.SubElement(offer, "vat").text = f"{str(item_vat)}"

            shipment_option = ET.SubElement(offer, "shipment-options")
            ET.SubElement(shipment_option, "option", attrib={"days": "1", "order-before": "15"})

            ET.SubElement(offer, "vendor").text = f"{item.trademark}"
            ET.SubElement(offer, "vendorCode").text = f"{str(item.sid)}"

            barcode = ''
            try:
                for i in ast.literal_eval(item.attrs):
                    if i['numrange_value']:
                        code = str(ast.literal_eval(i['numrange_value'])[0])
                        if not code.startswith('2') and not code.startswith('1') and len(code) > 8:
                            barcode = code
                            break
            except:
                pass

            ET.SubElement(offer, "barcode").text = f"{str(barcode)}"
            # ET.SubElement(offer, "model").text = "Indesit SB 185"

            item_description = re.sub(r"<[^>]+>", "", item.description, flags=re.S)

            ET.SubElement(offer, "description").text = f"{item_description}"

            outlets = ET.SubElement(offer, "outlets")

            ET.SubElement(outlets, "outlet",
                          attrib={"id": "125735", "instock": f"{str(item.stocks)}", "price": f"{str(item_price)}",
                                  "oldprice": f"{str(item_price_max)}"})

            param1 = ET.SubElement(offer, "param", attrib={"name": "Материал"})
            param1.text = f"{item.stuff}"

        te = time.time()
        logger.info(f'Creating items finished in {te - ts:.2f} seconds')

        ts = time.time()
        logger.info(f'Creating XML file {file}...')

        tree = ET.ElementTree(root)
        tree.write(path, encoding="UTF-8", xml_declaration=True)

        te = time.time()
        logger.info(f'Creating XML file {file} finished in {te - ts:.2f} seconds')

        ts = time.time()
        logger.info('Writing XML file to DB...')

        # XMLFeed.objects.create(file=file)
        await XMLFeed.objects.aupdate_or_create(defaults={'file': file}, id=counter)

        te = time.time()
        logger.info(f'Writing XML file to DB finished in {te - ts:.2f} seconds')
        counter += 1


async def main():
    try:
        while True:
            try:
                os.system('systemctl stop aioparser.service')
                await asyncio.sleep(5)

                # XMLFeed.objects.filter(pk__gte=1).delete()

                total = SimaItem.objects.all().count()
                await create_xml(max_count=total, file_count=10)

                os.system('systemctl start aioparser.service')
                await asyncio.sleep(60 * 60 * 3)  # seconds * minutes * hours
            except OperationalError:
                ...
                # os.system('systemctl restart yml.service')
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(main())
