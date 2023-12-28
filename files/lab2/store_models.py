from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Модель определяющая общие свойства продукта"""
    name = models.CharField(
        max_length=255,
        verbose_name="название"
    )  # Название товара

    slug_name = models.SlugField(
        verbose_name="'slug' значение"
    )  # Slug название товара

    description = models.TextField(
        verbose_name="описание"
    )  # Описание товара

    unit = models.ForeignKey(
        'Unit',
        on_delete=models.CASCADE,
        verbose_name="размерность"
    )  # Размерность

    quantity_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="количество за ед.",
        help_text="количество товара в единице размерности (1.000 кг; 0.500 л)"
    )  # Значение у размерности

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="цена"
    )  # Цена без учета скидки

    currency = models.ForeignKey(
        'Currency',
        on_delete=models.CASCADE,
        verbose_name="валюта"
    )  # Ссылка на валюту цены

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name="категория"
    )  # Ссылка на категорию

    image = models.ImageField(
        upload_to='static/products/',
        help_text="Загрузите картинку (желательно, но не обязательно). "
                  "Картинка загрузится в папку static/products/",
        verbose_name="картинка",
        null=True,
        blank=True,
    )  # Картинка товара

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"Продукт: {self.name!r}, Категория: {self.category.name!r}, " \
               f"Цена = {self.price} за {self.quantity_per_unit} {self.unit.name}"

    class Meta:
        verbose_name = 'Продукт'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Продукты'  # множественная форма (для отображения в админ панели)


class ProductDetail(models.Model):
    """Модель определяющая дополнительные поля продукта"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт",
        related_name='details',
    )  # Ссылка на продукт

    rating_mean = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2,
        verbose_name="средний рейтинг"
    )  # Средний рейтинг

    review_count = models.PositiveIntegerField(
        default=0,
        verbose_name="число отзывов"
    )  # Число отзывов

    sold_value = models.PositiveIntegerField(
        default=0,
        verbose_name="количество продаж"
    )  # Объём проданного товара

    quantity_in_stock = models.PositiveIntegerField(
        default=0,
        verbose_name="количество на складе"
    )  # Загрузка товара на складе

    is_available = models.BooleanField(
        default=True,
        verbose_name="доступность к покупке"
    )  # Доступность данного варианта продукта к продаже

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"Продукт: {self.product.name}; Рейтинг = {self.rating_mean}"

    class Meta:
        verbose_name = 'Подробности о продукте'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Подробности о продуктах'  # множественная форма (для отображения в админ панели)


class Unit(models.Model):
    """Модель определяющая размерность"""
    name = models.CharField(
        max_length=50,
        verbose_name="название"
    )  # Название размерности

    description = models.TextField(
        null=True,
        verbose_name="описание"
    )  # Описание размерности

    conversion_factor = models.FloatField(
        default=1.0,
        verbose_name="коэффициент",
        help_text="Коэффициент для перевода к стандартным величинам "
                  "(допустим из грамм в килограммы и т.д.)"
    )  # Коэффициент для перевода к стандартным величинам (допустим из грамм в килограммы и т.д.)

    created_at = models.DateTimeField(
        auto_now_add=True)  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размерность'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Размерности'  # множественная форма (для отображения в админ панели)


class Currency(models.Model):
    """Модель определяющая валюту"""
    name = models.CharField(
        max_length=50,
        verbose_name="название",
    )  # Название валюты

    description = models.TextField(
        null=True,
        verbose_name="описание"
    )  # Описание валюты

    currency_sign = models.CharField(
        max_length=50,
        default='₽',
        verbose_name="отображение знака",
        help_text="Значение, для подстановки в HTML. &#x20bd - знак рубля"
    )  # Значение, для подстановки в HTML. &#x20bd - знак рубля

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    class Meta:
        verbose_name = 'Валюта'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Валюты'  # множественная форма (для отображения в админ панели)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель определяющая категория с возможностью вложенных категорий"""
    name = models.CharField(
        max_length=255,
        verbose_name="название",
    )  # Название категории

    slug_name = models.SlugField(
        unique=True,
        verbose_name="'slug' значение",
    )  # Название категории для передачи в адресную строку

    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children',
                               verbose_name="родительская категория",
                               )

    created_at = models.DateTimeField(
        auto_now_add=True)  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    class Meta:
        unique_together = ('slug_name',
                           'parent',)  # Для проверки, что у одной базовой категории нет такого же slug
        verbose_name = 'Категория'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Категории'  # множественная форма (для отображения в админ панели)

    def __str__(self):
        return self.name


class ProductDiscount(models.Model):
    """Модель скидка на продукт"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='discount',
        verbose_name='продукт'
    )

    value = models.PositiveIntegerField(
        verbose_name='значение скидки'
    )

    is_percentage = models.BooleanField(
        default=True,
        verbose_name='процентная скидка',
        help_text="Если не процентная, то по постоянное значение"
    )
    start_date = models.DateTimeField(
        verbose_name='Дата и время начала действия скидки',
    )  # Дата и время начала действия скидки

    end_date = models.DateTimeField(
        verbose_name='Дата и время окончания действия скидки',
    )  # Дата и время окончания действия скидки

    is_active = models.BooleanField(
        default=True,
        verbose_name='скидка активна',
    )  # Флаг активности скидки

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"{self.value}" \
               f"{'%' if self.is_percentage else ''} " \
               f"скидка на продукт {self.product.name!r}" \
               f" с {self.start_date} по {self.end_date}"

    class Meta:
        verbose_name = 'Скидка на продукты'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Скидки на продукты'  # множественная форма (для отображения в админ панели)


class Review(models.Model):
    """Модель для отзывов"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт",
        related_name="reviews",
    )  # Ссылка на продукт

    rating = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2,
        verbose_name="оценка"
    )  # Рейтинг отзыва(оценка).

    comment = models.TextField(
        verbose_name="текст отзыва"
    )  # Текст отзыва

    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Ссылка на пользователя. При удалении пользователя из БД - его отзывы не удаляются
        null=True,
        verbose_name="пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"Продукт: {self.product.name}, Рейтинг: {self.rating}, Пользователь: {self.customer.username}"

    class Meta:
        verbose_name = 'Отзыв'  # одиночная форма (для отображения в админ панели)
        verbose_name_plural = 'Отзывы'  # множественная форма (для отображения в админ панели)