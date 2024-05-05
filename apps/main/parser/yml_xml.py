import sys
import time

import django
import os
import ast
from pathlib import Path
import logging
import re
from datetime import datetime
import xml.etree.ElementTree as ET

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
django.setup()
from apps.main.models import *
from apps.main.parser import prices

local_time = datetime.now().strftime('%Y-%m-%dT%H:%M+05:00')
path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("static").joinpath("media") / 'offers.xml'
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

# Создайте корневой элемент каталога
root = ET.Element("yml_catalog", attrib={"date": f"{local_time}"})

# Создайте элемент магазина
shop = ET.SubElement(root, "shop")

# Создайте элемент категорий
ts = time.time()
categories = ET.SubElement(shop, "categories")
cts = set()
logger.info('Creating categories...')

# Создайте элементы категорий
for item in iter(SimaItem.objects.all()[40000:80000]):
    cts.add(ast.literal_eval(item.categories)[0])

logger.info('Adding categories to XML ...')
for cat_id in cts:
    ET.SubElement(categories, "category", attrib={"id": f"{str(cat_id)}"})  # "parentId": "3798"
te = time.time()
logger.info(f'Creating categories finished in {te - ts:.2f} seconds')

# Создайте элемент вариантов доставки
shipment_options = ET.SubElement(shop, "shipment-options")

# Создайте элемент варианта доставки
option = ET.SubElement(shipment_options, "option", attrib={"days": "1", "order-before": "15"})

# Создайте элемент предложений
offers = ET.SubElement(shop, "offers")

ts = time.time()
logger.info('Creating items...')

# Создайте элемент предложения
for item in iter(SimaItem.objects.all()[40000:80000]):
    offer = ET.SubElement(offers, "offer", attrib={"id": f"{str(item.item_id)}", "available": "true"})

    # Создайте элементы предложения
    # ET.SubElement(offer, "url").text = "http://www.abc.ru/158.html"

    item_name = item.name
    if item.min_qty > 1:
        item_name = f"{item_name} ({str(item.min_qty)} шт.)"
        # print(item_name, item.min_qty)
    ET.SubElement(offer, "name").text = f"{item_name}"

    item_price = float(item.price) * item.min_qty
    item_price_max = float(item.price_max) * item.min_qty

    for p in prices.price_ratio:
        if p[0] >= float(item_price):
            item_price = float(item_price) * p[1]
            item_price_max = float(item_price_max) * p[1]
            break
    ET.SubElement(offer, "price").text = f"{str(item_price)}"
    ET.SubElement(offer, "oldprice").text = f"{str(item_price_max)}"

    ET.SubElement(offer, "categoryId").text = f"{str(ast.literal_eval(item.categories)[0])}"
    ET.SubElement(offer, "picture").text = f"{item.photo_url}"

    item_vat = 0
    if int(item.vat) == 20:
        item_vat = 1
    elif int(item.vat) == 10:
        item_vat = 2
    ET.SubElement(offer, "vat").text = f"{str(item_vat)}"

    # Создайте вложенный элемент варианта доставки
    shipment_option = ET.SubElement(offer, "shipment-options")
    ET.SubElement(shipment_option, "option", attrib={"days": "1", "order-before": "15"})

    ET.SubElement(offer, "vendor").text = f"{item.trademark}"
    ET.SubElement(offer, "vendorCode").text = f"{str(item.sid)}"
    try:
        tnved = item.attrs.split("'tnved',")[-1].split("'value': ")[1].split(",")[0].strip()
    except:
        tnved = ""
    # ET.SubElement(offer, "barcode").text = f"{tnved}"
    ET.SubElement(offer, "barcode").text = f""
    # ET.SubElement(offer, "model").text = "Indesit SB 185"

    item_description = re.sub(r"<[^>]+>", "", item.description, flags=re.S)

    ET.SubElement(offer, "description").text = f"{item_description}"
    ET.SubElement(offer, "description").text = f"{item_description}"

    # Создайте элемент магазинов
    outlets = ET.SubElement(offer, "outlets")

    # Создайте элементы магазинов
    ET.SubElement(outlets, "outlet", attrib={"id": "125735", "instock": f"{str(item.stocks)}", "price": f"{str(item_price)}", "oldprice": f"{str(item_price_max)}"})

    # Добавьте параметры
    param1 = ET.SubElement(offer, "param", attrib={"name": "Материал"})
    param1.text = f"{item.stuff}"
    #
    # param2 = ET.SubElement(offer, "param", attrib={"name": ""})
    #
    # param3 = ET.SubElement(offer, "param", attrib={"name": ""})

te = time.time()
logger.info(f'Creating items finished in {te - ts:.2f} seconds')

ts = time.time()
logger.info('Creating XML file...')

# Записываем XML-дерево в файл
tree = ET.ElementTree(root)
tree.write(path, encoding="UTF-8", xml_declaration=True)

te = time.time()
logger.info(f'Creating XML file finished in {te - ts:.2f} seconds')

ts = time.time()
logger.info('Writing XML file to DB...')

# XMLFeed.objects.filter(pk__gte=1).delete()
# XMLFeed.objects.create(file='offers.xml')

te = time.time()
logger.info(f'Writing XML file to DB finished in {te - ts:.2f} seconds')
