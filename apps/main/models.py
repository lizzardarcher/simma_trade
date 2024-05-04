from django.db import models


class SimaItem(models.Model):
    item_id = models.PositiveIntegerField(unique=True, primary_key=True)
    sid = models.PositiveIntegerField(null=True, )
    name = models.CharField(null=True, max_length=255)
    minimum_order_quantity = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    price = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    price_max = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    currency = models.CharField(null=True, max_length=3)
    boxtype_id = models.PositiveIntegerField(null=True, )
    box_depth = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    box_height = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    box_width = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    in_box = models.PositiveIntegerField(null=True, )
    in_set = models.PositiveIntegerField(null=True, )
    depth = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    unit_id = models.PositiveIntegerField(null=True, )
    width = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    height = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    max_qty = models.PositiveIntegerField(null=True, )
    min_qty = models.PositiveIntegerField(null=True, )
    vat = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    supplier_code = models.CharField(null=True, max_length=50)
    weight = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0)
    photo_url = models.URLField(null=True, blank=True)
    package_volume = models.DecimalField(null=True, max_digits=10, decimal_places=3)
    product_volume = models.DecimalField(null=True, max_digits=20, decimal_places=15)
    box_volume = models.DecimalField(null=True, max_digits=30, decimal_places=15)
    box_capacity = models.PositiveIntegerField(null=True, )
    img = models.URLField(null=True, blank=True)
    size = models.CharField(null=True, max_length=50)
    stuff = models.CharField(null=True, max_length=100)
    trademark = models.CharField(null=True, max_length=100, blank=True)
    categories = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    stocks = models.TextField(null=True, blank=True)
    attrs = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар Сима Лэнд'
        verbose_name_plural = 'Товары Сима Лэнд'


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(null=True, max_length=100)
    full_name = models.CharField(null=True, max_length=255)
    alpha2 = models.CharField(null=True, max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна производитель'
        verbose_name_plural = 'Страны производители'


class SimaCategory(models.Model):
    cat_id = models.PositiveIntegerField(unique=True, primary_key=True)
    sid = models.PositiveIntegerField(null=True, )
    name = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория Сима Лэнд'
        verbose_name_plural = 'Категории Сима Лэнд'


class SimaFilter(models.Model):
    filter_id = models.PositiveIntegerField(unique=True, primary_key=True)
    max_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name='Максимальная цена')
    min_stock = models.PositiveIntegerField(null=True, verbose_name='Минимальный остаток на складе')
    max_width = models.PositiveIntegerField(null=True, blank=True, verbose_name='Максимальная Ширина')
    min_width = models.PositiveIntegerField(null=True, blank=True, verbose_name='Минимальная Ширина')
    max_height = models.PositiveIntegerField(null=True, blank=True, verbose_name='Максимальная Высота')
    min_height = models.PositiveIntegerField(null=True, blank=True, verbose_name='Минимальная Высота')
    max_depth = models.PositiveIntegerField(null=True, blank=True, verbose_name='Максимальная Глубина')
    min_depth = models.PositiveIntegerField(null=True, blank=True, verbose_name='Минимальная Глубина')

    def __str__(self):
        return str(self.filter_id) + ' - Макс Цена: ' + str(self.max_price) + ' - Мин Остаток на складе' + str(
            self.min_stock)

    class Meta:
        verbose_name = 'Фильтр Сима Лэнд'
        verbose_name_plural = 'Фильтры Сима Лэнд'


class SimaSettings(models.Model):
    token = models.CharField(null=True, max_length=255, blank=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class SimaBlacklist(models.Model):
    categories = models.CharField(null=True, max_length=1000000, blank=True)
    items = models.CharField(null=True, max_length=1000000, blank=True)
    sellers = models.CharField(null=True, max_length=1000000, blank=True)

    def __str__(self):
        return 'Black List'


class XMLFeed(models.Model):
    file = models.FileField()

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'XML Feed'
        verbose_name_plural = 'XML Feed'
