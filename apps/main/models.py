from django.db import models


class SimaItem(models.Model):
    item_id = models.PositiveIntegerField(unique=True, primary_key=True)
    sid = models.PositiveIntegerField(null=True, )
    uid = models.UUIDField(null=True, )
    name = models.CharField(null=True, max_length=255)
    slug = models.SlugField(null=True, max_length=255)
    is_disabled = models.CharField(max_length=255, null=True, default='')
    reason_of_disabling = models.CharField(null=True, max_length=255, blank=True)
    minimum_order_quantity = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    price = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    price_max = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    price_per_square_meter = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    price_per_linear_meter = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    currency = models.CharField(null=True, max_length=3)
    created_at = models.DateTimeField(null=True, )
    updated_at = models.DateTimeField(null=True, )
    boxtype_id = models.PositiveIntegerField(null=True, )
    box_depth = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    box_height = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    box_width = models.DecimalField(null=True, max_digits=20, decimal_places=10)

    in_box = models.PositiveIntegerField(null=True, )
    in_set = models.PositiveIntegerField(null=True, )
    depth = models.DecimalField(null=True, max_digits=20, decimal_places=10)

    unit_id = models.PositiveIntegerField(null=True, )
    nested_unit_id = models.PositiveIntegerField(null=True, blank=True)
    width = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    height = models.DecimalField(null=True, max_digits=20, decimal_places=10)

    trademark_id = models.PositiveIntegerField(null=True, blank=True)
    country_id = models.PositiveIntegerField(null=True, )
    cart_min_diff = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    keep_package = models.CharField(max_length=255, null=True, default='')
    per_package = models.PositiveIntegerField(null=True, )

    page_title = models.CharField(null=True, max_length=255, blank=True)
    page_keywords = models.CharField(null=True, max_length=255, blank=True)
    page_description = models.CharField(null=True, max_length=255, blank=True)
    parent_item_id = models.PositiveIntegerField(null=True, )
    max_qty = models.PositiveIntegerField(null=True, )
    min_qty = models.PositiveIntegerField(null=True, )
    modifier_id = models.PositiveIntegerField(null=True, blank=True)
    modifier_value = models.CharField(null=True, max_length=255, blank=True)
    qty_multiplier = models.PositiveIntegerField(null=True, )

    type = models.IntegerField(null=True, default=0)
    vat = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    currency_sign = models.CharField(null=True, max_length=50)
    is_enough = models.BooleanField(null=True, default=True)
    supplier_code = models.CharField(null=True, max_length=50)
    weight = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0)
    photo_url = models.URLField(null=True, blank=True)

    package_volume = models.DecimalField(null=True, max_digits=10, decimal_places=3)
    min_age = models.PositiveIntegerField(null=True, blank=True)
    power = models.CharField(null=True, max_length=255, blank=True)
    volume = models.CharField(null=True, max_length=255, blank=True)
    surface_area = models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)
    linear_meters = models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)
    is_boxed = models.CharField(max_length=255, null=True, default='')
    product_volume = models.DecimalField(null=True, max_digits=20, decimal_places=15)
    box_volume = models.DecimalField(null=True, max_digits=30, decimal_places=15)
    box_capacity = models.PositiveIntegerField(null=True, )
    packing_volume_factor = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    isbn = models.CharField(null=True, max_length=255)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    is_add_to_cart_multiple = models.BooleanField(null=True, default=True)
    supply_period = models.PositiveIntegerField(null=True, )
    is_remote_store = models.CharField(max_length=255, null=True, default='')
    min_sum_order = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    color = models.CharField(null=True, max_length=50, blank=True)
    image_title = models.CharField(null=True, max_length=255, blank=True)
    image_alt = models.CharField(null=True, max_length=255, blank=True)
    short_name = models.CharField(null=True, max_length=100, blank=True)
    min_sum_for_free_delivery = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    updated_item_at = models.DateTimeField(null=True, blank=True)
    img = models.URLField(null=True, blank=True)
    real_min_qty = models.PositiveIntegerField(null=True, default=100)
    item_url = models.CharField(null=True, max_length=255, blank=True)
    price_unit = models.CharField(null=True, max_length=50, blank=True)
    modifiers_count = models.IntegerField(null=True, blank=True)
    size = models.CharField(null=True, max_length=50)
    stuff = models.CharField(null=True, max_length=100)
    trademark = models.CharField(null=True, max_length=100, blank=True)
    series = models.CharField(null=True, max_length=100, blank=True)

    """### New"""
    materials                            = models.TextField(null=True, blank=True)
    authors                         = models.TextField(null=True, blank=True)
    notices                         = models.TextField(null=True, blank=True)
    files                         = models.TextField(null=True, blank=True)
    categories                         = models.TextField(null=True, blank=True)
    all_categories                         = models.TextField(null=True, blank=True)
    modifier_items                         = models.TextField(null=True, blank=True)
    description                         = models.TextField(null=True, blank=True)
    ext_description                         = models.TextField(null=True, blank=True)
    extra_notices                         = models.TextField(null=True, blank=True)
    stocks                         = models.TextField(null=True, blank=True)
    attrs                         = models.TextField(null=True, blank=True)

    # video_file_name = models.CharField(null=True, max_length=255, blank=True)
    # video_cover_file_name = models.CharField(null=True, max_length=255, blank=True)
    # video_file_url = models.CharField(max_length=255, null=True, default='')
    # series_id = models.PositiveIntegerField(null=True, blank=True)
    # is_hit = models.CharField(max_length=255, null=True, default='')
    # is_licensed = models.CharField(max_length=255, null=True, default='')
    # is_price_fixed = models.CharField(max_length=255, null=True, default='')
    # is_exclusive = models.CharField(max_length=255, null=True, default='')
    # is_motley = models.CharField(max_length=255, null=True, default='')
    # is_adult = models.CharField(max_length=255, null=True, default='')
    # is_protected = models.CharField(max_length=255, null=True, default='')
    # offer_id = models.PositiveIntegerField(null=True, blank=True)
    # certificate_type_id = models.PositiveIntegerField(null=True, )
    # has_usb = models.CharField(max_length=255, null=True, default='')
    # has_battery = models.CharField(max_length=255, null=True, default='')
    # has_clockwork = models.CharField(max_length=255, null=True, default='')
    # has_sound = models.CharField(max_length=255, null=True, default='')
    # has_radiocontrol = models.CharField(max_length=255, null=True, default='')
    # is_inertial = models.CharField(max_length=255, null=True, default='')
    # is_on_ac_power = models.CharField(max_length=255, null=True, default='')
    # has_rus_voice = models.CharField(max_length=255, null=True, default='')
    # has_rus_pack = models.CharField(max_length=255, null=True, default='')
    # has_light = models.CharField(max_length=255, null=True, default='')
    # is_day_offer = models.CharField(max_length=255, null=True, default='')
    # gift_id = models.PositiveIntegerField(null=True, blank=True)
    # is_loco = models.CharField(max_length=255, null=True, default='')
    # novelted_at = models.DateTimeField(null=True, blank=True)
    # is_paid_delivery = models.CharField(max_length=255, null=True, default='')
    # transport_condition_id = models.PositiveIntegerField(null=True, blank=True)
    # has_discount = models.BooleanField(null=True, default=True)
    # is_gift = models.CharField(max_length=255, null=True, default='')
    # is_tire_spike = models.CharField(max_length=255, null=True, default='')
    # is_tire_run_flat = models.CharField(max_length=255, null=True, default='')
    # tire_season_id = models.PositiveIntegerField(null=True, )
    # tire_diameter_id = models.PositiveIntegerField(null=True, )
    # tire_width_id = models.PositiveIntegerField(null=True, )
    # tire_section_height_id = models.PositiveIntegerField(null=True, )
    # tire_load_index_id = models.PositiveIntegerField(null=True, )
    # tire_speed_index_id = models.PositiveIntegerField(null=True, )
    # wheel_lz_id = models.PositiveIntegerField(null=True, )
    # wheel_width_id = models.PositiveIntegerField(null=True, )
    # wheel_diameter_id = models.PositiveIntegerField(null=True, )
    # wheel_dia_id = models.PositiveIntegerField(null=True, )
    # wheel_pcd_id = models.PositiveIntegerField(null=True, )
    # wheel_et_id = models.PositiveIntegerField(null=True, )
    # has_body_drawing = models.CharField(max_length=255, null=True, default='')
    # has_cord_case = models.CharField(max_length=255, null=True, default='')
    # has_teapot = models.CharField(max_length=255, null=True, default='')
    # has_termostat = models.CharField(max_length=255, null=True, default='')
    # is_imprintable = models.CharField(max_length=255, null=True, default='')
    # has_action = models.CharField(max_length=255, null=True, default='')
    # has_action_discount_system = models.CharField(max_length=255, null=True, default='')
    # has_jewelry_action = models.CharField(max_length=255, null=True, default='')
    # has_3_pay_2_action = models.CharField(max_length=255, null=True, default='')
    # has_best_fabric = models.CharField(max_length=255, null=True, default='')
    # has_best_textile = models.CharField(max_length=255, null=True, default='')
    # has_number_one_made_in_russia = models.CharField(max_length=255, null=True, default='')
    # audio_filename = models.CharField(null=True, max_length=255, blank=True)
    # photo_3d_count = models.IntegerField(null=True, blank=True)
    # is_markdown = models.CharField(max_length=255, null=True, default='')
    # is_prepay_needed = models.CharField(max_length=255, null=True, default='')
    # is_paid_delivery_ekb = models.CharField(max_length=255, null=True, default='')
    # mean_rating = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    # comments_count = models.IntegerField(null=True, default=0)
    # markdown_reason = models.CharField(null=True, max_length=255, blank=True)
    # is_wholesale = models.CharField(max_length=255, null=True, default='')
    # is_wholesale_conservation = models.CharField(max_length=255, null=True, default='')
    # is_shock_price = models.CharField(max_length=255, null=True, default='')
    # is_recommended = models.CharField(max_length=255, null=True, default='')
    # is_export_to_s3 = models.CharField(max_length=255, null=True, default='')
    # qty_rule = models.CharField(null=True, max_length=50)
    # qty_rules = models.CharField(null=True, max_length=255)
    # custom_qty_rules_data = models.JSONField(null=True, blank=True)
    # plural_name_format = models.CharField(null=True, max_length=50)
    # in_box_plural_name_format = models.CharField(null=True, max_length=50)
    # balance_plural_name_format = models.CharField(null=True, max_length=50, blank=True)
    # can_buy_by_credit = models.CharField(max_length=255, null=True, default='')
    # has_special_offer = models.CharField(max_length=255, null=True, default='')
    # has_day_discount = models.CharField(max_length=255, null=True, default='')
    # has_erich_krause = models.CharField(max_length=255, null=True, default='')
    # has_tm_gamma_gifts = models.CharField(max_length=255, null=True, default='')
    # has_superprice_on_line = models.CharField(max_length=255, null=True, default='')
    # has_week_discount = models.CharField(max_length=255, null=True, default='')
    # has_3days_discount = models.CharField(max_length=255, null=True, default='')
    # has_best_fabric_2018 = models.CharField(max_length=255, null=True, default='')
    # has_pay_later = models.CharField(max_length=255, null=True, default='')
    # has_new_rules = models.CharField(max_length=255, null=True, default='')
    # has_item_month = models.CharField(max_length=255, null=True, default='')
    # has_batteries_gift = models.CharField(max_length=255, null=True, default='')
    # special_offer_id = models.IntegerField(null=True, blank=True)
    # has_4_pay_2_action = models.CharField(max_length=255, null=True, default='')
    # has_take_installments_action = models.CharField(max_length=255, null=True, default='')
    # wholesale_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    # wholesale_price_text = models.CharField(null=True, max_length=100, blank=True)
    # is_part = models.CharField(max_length=255, null=True, default='')
    # is_small_wholesale_available = models.BooleanField(null=True, default=True)
    # is_plant = models.CharField(max_length=255, null=True, default='')
    # is_free_delivery = models.BooleanField(null=True, default=True)
    # nested_unit = models.CharField(null=True, max_length=50, blank=True)
    # is_entrance_type_by_weight = models.BooleanField(null=True, default=True)
    # is_weighted_goods = models.CharField(max_length=255, null=True, default='')
    # offer = models.CharField(null=True, max_length=100, blank=True)
    # discount_percent = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    # has_gift = models.CharField(max_length=255, null=True, default='')
    # has_gift_assignee = models.CharField(max_length=255, null=True, default='')
    # is_novelty = models.CharField(max_length=255, null=True, default='')
    # has_volume_discount = models.CharField(max_length=255, null=True, default='')
    # ecommerce_variant = models.CharField(null=True, max_length=50)
    # loan_category_id = models.IntegerField(null=True, blank=True)
    # transit_in_settlement = models.CharField(null=True, max_length=50, blank=True)
    # is_item_description_hidden = models.CharField(max_length=255, null=True, default='')
    # is_found_cheaper_enabled = models.CharField(max_length=255, null=True, default='')
    # wholesale_price_unit = models.CharField(null=True, max_length=50, blank=True)
    # wholesale_text = models.CharField(null=True, max_length=100)
    # arrival_date = models.DateTimeField(null=True, blank=True)
    # is_available_in_giper = models.CharField(max_length=255, null=True, default='')
    # retail_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    # video_cover_url = models.URLField(null=True, blank=True)

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
