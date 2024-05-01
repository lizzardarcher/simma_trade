import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sima_trade.settings")
django.setup()
from apps.main.models import *
import xlsxwriter
import ast
import html

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet('Список товаров')

worksheet.write('A1', 'id')
worksheet.write('B1', 'Доступность товара')
worksheet.write('C1', 'Категория')
worksheet.write('D1', 'Производитель (Бренд)')
worksheet.write('E1', 'Артикул')
worksheet.write('F1', 'Модель')
worksheet.write('G1', 'Название')
worksheet.write('H1', 'Цена(руб)')
worksheet.write('I1', 'Старая цена(руб)')
worksheet.write('J1', 'Остаток')
worksheet.write('K1', 'НДС')
worksheet.write('L1', 'Штрихкод')
worksheet.write('M1', 'Ссылка на картинку')
worksheet.write('N1', 'Описание')
worksheet.write('O1', 'Ссылка на товар на сайте магазина')
worksheet.write('P1', 'Время заказа До')
worksheet.write('Q1', 'Дней на отгрузку')

worksheet.write('A2', 'offer_id')
worksheet.write('B2', 'available')
worksheet.write('C2', 'category')
worksheet.write('D2', 'vendor')
worksheet.write('E2', 'vendor_code')
worksheet.write('F2', 'model')
worksheet.write('G2', 'name')
worksheet.write('H2', 'price')
worksheet.write('I2', 'old_price')
worksheet.write('J2', 'instock')
worksheet.write('K2', 'vat')
worksheet.write('L2', 'barcode')
worksheet.write('M2', 'picture')
worksheet.write('N2', 'description')
worksheet.write('O2', 'url')
worksheet.write('P2', 'order-before')
worksheet.write('Q2', 'days')

items = [(x.item_id, 'Доступен', ast.literal_eval(x.categories)[0], x.trademark, x.sid, 'Россия', x.name, x.price, x.price_max, 100,
        x.vat, '', x.photo_url, x.description, '', 23, '1 день') for x in SimaItem.objects.all()]

# Start from the first cell. Rows and columns are zero indexed.
row = 2
# row = 0
col = 0

# Iterate over the data and write it out row by row.
for item in items:
    # worksheet.write(row, col, item)
    worksheet.write(row, col+0,  item[0])
    worksheet.write(row, col+1,  item[1])
    worksheet.write(row, col+2,  item[2])
    worksheet.write(row, col+3,  item[3])
    worksheet.write(row, col+4,  item[4])
    worksheet.write(row, col+5,  item[5])
    worksheet.write(row, col+6,  item[6])
    worksheet.write(row, col+7,  item[7])
    worksheet.write(row, col+8,  item[8])
    worksheet.write(row, col+9, item[9])
    worksheet.write(row, col+10, item[10])
    worksheet.write(row, col+11, item[11])
    worksheet.write(row, col+12, item[12])
    worksheet.write(row, col+13, item[13])
    worksheet.write(row, col+14, item[14])
    worksheet.write(row, col+15, item[15])
    worksheet.write(row, col+16, item[16])
    row += 1


workbook.close()