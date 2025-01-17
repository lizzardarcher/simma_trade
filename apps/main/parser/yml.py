import os
import math
import sys
import time
import asyncio
import ast
import traceback
from pathlib import Path
import logging
import re
from datetime import datetime
import xml.etree.ElementTree as ET
from logging.handlers import RotatingFileHandler
import django

from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
django.setup()

from apps.main.models import *
from apps.main.parser import prices
from apps.main.parser.progress import bar
from apps.main.parser.progress import colors

os.environ["PYTHONMAXSIZE"] = str(3221225472)
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


def is_filter_success(item: SimaItem, filters: dict, black_list: dict) -> bool:
    """
    Фильтр по заданным в БД значениям и по Черному списку
    Возвращает True, если товар проходит по фильтрам и по ЧС
    :param item: SimaItem model
    :param filters: SimaFilter model
    :param black_list: SimaBlackList model
    :return: bool
    """
    check = False
    if ((int(filters['min_depth']) <= int(item.box_depth) < int(filters['max_depth']) and
            int(filters['min_height']) <= int(item.box_height) < int(filters['max_height']) and
            int(filters['min_width']) <= int(item.box_width) < int(filters['max_width']) and
            int(item.price) <= int(filters['max_price'])) and
            (int(item.price) * int(item.min_qty)) <= int(filters['max_price'])):
        if item.trademark.lower() not in black_list['black_tms'] and item.sid not in black_list['black_sids']:
            for c in ast.literal_eval(item.categories):
                if int(c) in black_list['black_cats']:
                    check = False
                    break
                check = True
    return check


def cleared_string(string: str):
    """
    Обработка строки с заменой символов в соответствии с требованиями к XML файлам сервиса Megamarket
    '>'  -->  '&gt;'
    '<'  -->  '&lt;'
    "'"  -->  '&apos;'
    '&'  -->  '&amp;'
    '"'  -->  '&quot;'
    """
    string = string.replace('>', '&gt;').replace('<', '&lt;')
    string = string.replace('&', '&amp;').replace("'", "&apos;").replace('"', '&quot;')
    return string


# todo Создаётся один лишний пустой последний файл. Некритично, но желательно разобраться
async def create_xml(max_count, file_count):
    """
    Асинхронная функция создания XML фида для выгрузки на мегамаркет
    :param max_count: Общее количество товаров
    :param file_count: Количество создаваемых файлов
    """

    #  Местное время в соответствии с требованиями Megamarket
    # И возможно подойдёт для YandexMarket и Ozon. Надо проверять
    local_time = datetime.now().strftime('%Y-%m-%dT%H:%M+05:00')

    stores = Store.objects.all()
    for store in stores:

        counter = 1
        l_ids = [x for x in range(1, max_count + 1)]
        chunk_size = math.floor(max_count / file_count)
        chunks = [l_ids[i:i + chunk_size] for i in range(0, len(l_ids), chunk_size)]
        pairs = [(chunk[0], chunk[-1]) for chunk in chunks]

        # current_cats = []
        # used_cats = []

        black_dict = {'black_tms': ast.literal_eval(store.blacklist.black_tm),
                      'black_cats': ast.literal_eval(store.blacklist.black_cat),
                      'black_sids': ast.literal_eval(store.blacklist.black_sids)
                      }
        filters_dict = {'max_width': store.sima_filter.max_width,
                        'min_width': store.sima_filter.min_width,
                        'max_height': store.sima_filter.max_height,
                        'min_height': store.sima_filter.min_height,
                        'max_depth': store.sima_filter.max_depth,
                        'min_depth': store.sima_filter.min_depth,
                        'max_price': store.sima_filter.max_price
                        }

        for pair in pairs:
            print('#' * 140)
            ts = time.time()
            file = f'offers-{store.slug}-{str(counter)}.xml'
            path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("static").joinpath("media") / file

            root = ET.Element("yml_catalog", attrib={"date": f"{local_time}"})
            shop = ET.SubElement(root, "shop")
            categories = ET.SubElement(shop, "categories")

            cts = set()
            logger.info(f'Создание файла: {file} ')

            items = SimaItem.objects.all().order_by('item_id')[pair[0]:pair[1]]
            items_count = items.count()

            bar1 = bar.ShadyBar('Подготовка списка категорий', max=items_count, suffix='%(percent)d%%')
            for item in iter(items):
                bar1.next()

                if is_filter_success(item=item, filters=filters_dict, black_list=black_dict):
                    for i in sorted(ast.literal_eval(item.categories)):
                        # if len(str(i)) <= 6:
                        cts.add(i)
            bar1.finish()

            bar2 = bar.ShadyBar('Создание списка категорий', max=len(cts), suffix='%(percent)d%%')
            for cat_id in cts:
                try:
                    ET.SubElement(categories, "category",
                                  attrib={
                                      "id": f"{str(cat_id)}"}).text = cleared_string(f"{SimaCategory.objects.get(cat_id=cat_id).name}")
                    bar2.next()
                except:
                    ET.SubElement(categories, "category", attrib={"id": f"{str(cat_id)}"})
                    bar2.next()
            bar2.finish()

            shipment_options = ET.SubElement(shop, "shipment-options")
            option = ET.SubElement(shipment_options, "option", attrib={"days": "1", "order-before": "15"})
            offers = ET.SubElement(shop, "offers")

            bar3 = bar.ShadyBar('Создание списка товаров', max=items_count, suffix='%(percent)d%%')
            for item in items:
                bar3.next()

                if is_filter_success(item=item, filters=filters_dict, black_list=black_dict):

                    offer = ET.SubElement(offers, "offer", attrib={"id": f"{str(item.item_id)}", "available": "true"})

                    # ET.SubElement(offer, "url").text = "http://www.abc.ru/158.html"

                    item_name = item.name
                    if item.min_qty > 1:
                        item_name = f"{item_name} ({str(item.min_qty)} шт.)"
                    ET.SubElement(offer, "name").text = cleared_string(f"{item_name}")

                    item_price = float(item.price) * item.min_qty
                    item_price_max = float(item.price_max) * item.min_qty

                    for p in prices.price_ratio:
                        if float(item_price) <= p[0]:
                            item_price = int(float(item_price) * p[1] * (1 - store.discount / 100))
                            item_price_max = int(float(item_price_max) * p[1] * (1 - store.discount / 100))
                            break

                    ET.SubElement(offer, "price").text = cleared_string(f"{str(item_price)}")
                    ET.SubElement(offer, "oldprice").text = cleared_string(f"{str(item_price_max)}")

                    ET.SubElement(offer, "categoryId").text = cleared_string(f"{sorted(ast.literal_eval(item.categories))[0]}")
                    ET.SubElement(offer, "picture").text = cleared_string(f"{item.photo_url}")

                    item_vat = 0
                    if int(item.vat) == 20:
                        item_vat = 1
                    elif int(item.vat) == 10:
                        item_vat = 2
                    ET.SubElement(offer, "vat").text = cleared_string(f"{str(item_vat)}")

                    shipment_option = ET.SubElement(offer, "shipment-options")
                    ET.SubElement(shipment_option, "option", attrib={"days": "1", "order-before": "15"})

                    ET.SubElement(offer, "vendor").text = cleared_string(f"{item.trademark}")
                    ET.SubElement(offer, "vendorCode").text = cleared_string(f"{str(item.sid)}")

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

                    ET.SubElement(offer, "barcode").text = cleared_string(f"{str(barcode)}")
                    # ET.SubElement(offer, "model").text = "Indesit SB 185"

                    item_description = re.sub(r"<[^>]+>", "", item.description, flags=re.S)

                    ET.SubElement(offer, "description").text = cleared_string(f"{item_description}")

                    outlets = ET.SubElement(offer, "outlets")

                    ET.SubElement(outlets, "outlet",
                                  attrib={"id": "125735", "instock": f"{str(item.stocks)}",
                                          "price": f"{str(item_price)}",
                                          "oldprice": f"{str(item_price_max)}"})

                    param1 = ET.SubElement(offer, "param", attrib={"name": "Материал"})
                    param1.text = cleared_string(f"{item.stuff}")

            bar3.finish()

            tree = ET.ElementTree(root)
            tree.write(path, encoding="UTF-8", xml_declaration=True)

            await XMLFeed.objects.aupdate_or_create(defaults={'file': file}, id=counter)
            counter += 1

            te = time.time()
            logger.info(f'Длина списка категорий {len(cts)}')
            logger.info(f'Длина списка товаров {items_count}')
            logger.info(
                f'Запись файла завершена за: {math.floor((te - ts) / 60)}:{math.floor((te - ts) % 60)} минут')


async def main():
    try:
        while True:
            try:
                os.system('systemctl stop aioparser.service')
                await asyncio.sleep(5)
                total = SimaItem.objects.all().count()
                await create_xml(max_count=total, file_count=5)
                await asyncio.sleep(4)
                os.system('systemctl start aioparser.service')
                await asyncio.sleep(60 * 60 * 6)  # seconds * minutes * hours
            except:
                print(traceback.format_exc())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(main())
