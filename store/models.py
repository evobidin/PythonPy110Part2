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


DATABASE = {'1': {'name': 'Болгарский перец',
                  'discount': 30,
                  'price_before': 300.00,
                  'price_after': 210.00,
                  'description': 'Сочный и яркий, он добавит красок и вкуса в ваши блюда.',
                  'rating': 4.9,
                  'review': 250,
                  'sold_value': 600,
                  'weight_in_stock': 500,
                  'category': 'Овощи',
                  'id': 1,
                  'url': 'store/images/product-1.jpg',
                  'html': 'bell_pepper'
                  },
            '2': {'name': 'Клубника',
                  'discount': None,
                  'price_before': 500.00,
                  'price_after': 500.00,
                  'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
                  'rating': 5.0,
                  'review': 200,
                  'sold_value': 700,
                  'weight_in_stock': 400,
                  'category': 'Фрукты',
                  'id': 2,
                  'url': 'store/images/product-2.jpg',
                  'html': 'strawberry'
                  },
            '3': {'name': 'Стручковая фасоль',
                  'discount': None,
                  'price_before': 250.00,
                  'price_after': 250.00,
                  'rating': 4.8,
                  'review': 250,
                  'sold_value': 500,
                  'weight_in_stock': 500,
                  'description': 'Зеленая натуральность и богатство белка для вашей здоровой диеты.',
                  'rating': 5.0,
                  'review': 100,
                  'sold_value': 500,
                  'weight_in_stock': 600,
                  'category': 'Овощи',
                  'id': 3,
                  'url': 'store/images/product-3.jpg',
                  'html': 'green_beans'
                  },
            '4': {'name': 'Краснокочанная капуста',
                  'discount': None,
                  'price_before': 90.00,
                  'price_after': 90.00,
                  'description': 'Удивите своих гостей экзотическим вкусом и цветом ваших блюд.',
                  'rating': 4.7,
                  'review': 30,
                  'sold_value': 50,
                  'weight_in_stock': 300,
                  'category': 'Овощи',
                  'id': 4,
                  'url': 'store/images/product-4.jpg',
                  'html': 'purple_cabbage'
                  },
            '5': {'name': 'Помидоры',
                  'discount': 25,
                  'price_before': 240.00,
                  'price_after': 180.00,
                  'description': 'Свежие и сочные помидоры для идеальных салатов и соусов.',
                  'rating': 4.9,
                  'review': 350,
                  'sold_value': 700,
                  'weight_in_stock': 300,
                  'category': 'Овощи',
                  'id': 5,
                  'url': 'store/images/product-5.jpg',
                  'html': 'tomatoes'
                  },
            '6': {'name': 'Брокколи',
                  'discount': None,
                  'price_before': 320.00,
                  'price_after': 320.00,
                  'description': 'Здоровье в каждом кусочке, чтобы укрепить вашу иммунную систему.',
                  'rating': 4.9,
                  'review': 150,
                  'sold_value': 250,
                  'weight_in_stock': 300,
                  'category': 'Овощи',
                  'id': 6,
                  'url': 'store/images/product-6.jpg',
                  'html': 'broccoli'
                  },
            '7': {'name': 'Морковь',
                  'discount': None,
                  'price_before': 50.00,
                  'price_after': 50.00,
                  'description': 'Красота и здоровье для ваших глаз и кожи в каждой моркови.',
                  'rating': 4.8,
                  'review': 220,
                  'sold_value': 800,
                  'weight_in_stock': 900,
                  'category': 'Овощи',
                  'id': 7,
                  'url': 'store/images/product-7.jpg',
                  'html': 'carrots'
                  },
            '8': {'name': 'Фруктовый сок',
                  'discount': None,
                  'price_before': 120.00,
                  'price_after': 120.00,
                  'description': 'Натуральная свежесть и энергия в каждом глотке.',
                  'rating': 4.9,
                  'review': 300,
                  'sold_value': 800,
                  'weight_in_stock': 1200,
                  'category': 'Соки',
                  'id': 8,
                  'url': 'store/images/product-8.jpg',
                  'html': 'fruit_juice'
                  },
            '9': {'name': 'Лук',
                  'discount': 20,
                  'price_before': 40.00,
                  'price_after': 32.00,
                  'description': 'Придайте особый аромат и вкус вашим блюдам с нашим свежим луком.',
                  'rating': 4.6,
                  'review': 80,
                  'sold_value': 170,
                  'weight_in_stock': 350,
                  'category': 'Овощи',
                  'id': 9,
                  'url': 'store/images/product-9.jpg',
                  'html': 'onion'
                  },
            '10': {'name': 'Яблоки',
                   'discount': None,
                   'price_before': 130.00,
                   'price_after': 130.00,
                   'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
                   'rating': 4.7,
                   'review': 30,
                   'sold_value': 70,
                   'weight_in_stock': 200,
                   'category': 'Фрукты',
                   'id': 10,
                   'url': 'store/images/product-10.jpg',
                   'html': 'apple'
                   },
            '11': {'name': 'Чеснок',
                   'discount': None,
                   'price_before': 150.00,
                   'price_after': 150.00,
                   'description': 'Секрет вкусных блюд и поддержания здоровья вашего сердца.',
                   'rating': 4.9,
                   'review': 150,
                   'sold_value': 400,
                   'weight_in_stock': 1000,
                   'category': 'Овощи',
                   'id': 11,
                   'url': 'store/images/product-11.jpg',
                   'html': 'garlic'
                   },
            '12': {'name': 'Перец Чили',
                   'discount': None,
                   'price_before': 400.00,
                   'price_after': 400.00,
                   'description': 'Острая страсть для тех, кто ищет приключения на своей тарелке.',
                   'rating': 5.0,
                   'review': 40,
                   'sold_value': 300,
                   'weight_in_stock': 50,
                   'category': 'Овощи',
                   'id': 12,
                   'url': 'store/images/product-12.jpg',
                   'html': 'chilli'
                   },
            }
