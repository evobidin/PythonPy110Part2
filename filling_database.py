"""
Заполнение данных в БД через скрипт python.
Для заполнения, достаточно просто запустить скрипт.

Так же приведенные команды в блоке (if __name__ == "__main__":)
можно аналогично выполнить в окружении запускаемом командой
python manage.py shell

В случае вызова консоли (python manage.py shell), то так же как и в
приведенном блоке (if __name__ == "__main__":) необходимо
импортировать модели с которыми будете работать и далее выполнять команды с БД.
"""

import django
import os
import asyncio
from time import time
from json import dump, load
from django.core.exceptions import ValidationError
from faker import Faker
from django.core.files import File

# from django.db import transaction
# import re
# from django.utils import timezone
# from asgiref.sync import sync_to_async
from datetime import date, datetime, timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, ProductDetail, Unit, Currency, Category, \
    ProductDiscount, DATABASE
from cart.models import Cart

project_directory = os.getcwd()  # Папка где был запущен скрипт

fake = Faker("ru")
Faker.seed(42)  # Фиксируем значение seed,
# чтобы случайные генерации были воспроизводимы


def create_admin(username, password, email, save_data=True):
    """Создаем администратора и записываем его, чтобы был доступ"""
    User.objects.create_superuser(username=username,
                                  password=password,
                                  email=email)
    if save_data:
        with open("admin.json", "w", encoding="utf-8") as f:
            dump({"username": username,
                  "email": email,
                  "password": password
                  }, f, indent=4)


def create_fake_users(num_users=10, save_data=True):
    """Создаем несуществующих пользователей и записываем их, чтобы был доступ"""
    t1 = time()
    data = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.free_email()
        password = fake.password()
        User.objects.create_user(username=username, email=email,
                                 password=password)
        data.append({"username": username,
                     "email": email,
                     "password": password
                     })
    print(
        f"Время выполнения создания {num_users} пользователей через цикл равно {time() - t1:.4f} c")
    if save_data:
        with open("users.json", "w", encoding="utf-8") as f:
            dump(data, f, indent=4)


async def async_create_fake_users(num_users=10):
    """Асинхронно создаем несуществующих пользователей"""
    t1 = time()
    data_user, data = [], []

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.free_email()
        password = fake.password()
        data_user.append(
            User(username=username, email=email, password=password))
        data.append({"username": username,
                     "email": email,
                     "password": password
                     })
    # У объекта БД есть метод save(), а для асинхронного сохранения применяют asave()
    await asyncio.gather(*[user.asave() for user in data_user])
    """
    asyncio.gather - это функция из библиотеки asyncio в Python, которая позволяет вам запускать 
    несколько корутин (асинхронных функций) параллельно и ожидать их завершения.
    В функцию передаются объекты (выполняемые функции), которые необходимо запустить асинхронно
    """

    print(
        f"Время выполнения создания {num_users} пользователей через асинхронный цикл равно {time() - t1:.4f} c")
    if os.path.exists("users.json"):
        with open("users.json", encoding="utf-8") as f:
            users = load(f)
        users += data  # Дозаписываем данные к уже имеющимся
        with open("users.json", "w", encoding="utf-8") as f:
            dump(users, f, indent=4)
    else:
        with open("users.json", "w", encoding="utf-8") as f:
            dump(data, f, indent=4)


def create_fake_users_with_bulk(num_users=10):
    """Создаем несуществующих пользователей с помощью работы с блоком данных bulk"""
    t1 = time()
    data = []
    try:
        for _ in range(num_users):
            username = fake.user_name()
            email = fake.free_email()
            password = fake.password()
            user = User(username=username, email=email, password=password)
            user.full_clean()  # Метод для валидации полей (можно не писать, если уверены, что поля валидны и данные можно сразу записывать в БД)
            data.append(user)
    except ValidationError as e:
        # Обработка ошибок валидации
        print(f"Ошибка валидации: {e}")
    except Exception as e:
        # Обработка других ошибок
        print(f"Произошла ошибка: {e}")
    else:
        User.objects.bulk_create(
            data)  # Если ошибок не было, то запишем пользователей одной записью
    print(
        f"Время выполнения создания {num_users} пользователей через bulk_create равно {time() - t1:.4f} c")


if __name__ == "__main__":
    """Создание пользователей"""
    create_admin("admin", "123", "admin@admin.com")
    create_fake_users()  # Работает долго, так как используется цикл и каждый раз создаётся транзакция в БД

    # Используем asyncio.run() для запуска асинхронной функции
    asyncio.run(
        async_create_fake_users())  # Работает намного быстрее чем стандартный цикл, так как все
    # транзакции отправляются почти параллельно и происходит ожидание когда процесс завершится.

    create_fake_users_with_bulk()  # Работает ещё быстрее, чем асинхронная функция, но не происходит
    # валидация полей перед сохранением (в конкретной реализации происходит за счёт вызова full_clean() внутри)
    # и вызов сигналов перед сохранением и после сохранения в БД.

    # Так как в create_fake_users_with_bulk не происходит вызовов сигналов на создание
    # корзин для пользователей, то это придётся сделать вручную. Проверим сколько
    # пользователей, а сколько корзин
    print(
        f"Всего пользователей {User.objects.count()}; Всего корзин для пользователей {Cart.objects.count()}")

    # Вручную получаем последние 10 пользователей и создаём для них корзины
    users = User.objects.all().order_by('-id')[
            :10]  # Последние 10 пользователей из БД
    # (слайсирование с отрицательным индексом не работает, поэтому производим сортировку
    # по убыванию id, берем первые 10 элементов)
    data = []
    for user in reversed(
            users):  # reversed чтобы привести к правильному порядку(так как из БД получили развернутый)
        data.append(Cart(customer=user))
    Cart.objects.bulk_create(
        data)  # Теперь можно использовать bulk для быстрого создания, так как проверки не нужны и зависимых сигналов нет.

    print(
        f"Всего пользователей {User.objects.count()}; Всего корзин для пользователей {Cart.objects.count()}")

    asyncio.run(async_create_fake_users(70))  # Допишем ещё 70 пользователей
    # в БД, чтобы общее число пользователей было равно 100

    print("___Пользователи созданы___")

    """Создание продуктов"""

    # Создание категорий. CATEGORY используется для более удобного доступа к объекту категории
    # так как продукт требует ссылку на категорию и будет необходимо передать объект категории,
    # а не просто имя
    CATEGORY = {
        "Овощи": Category.objects.create(name="Овощи", slug_name="vegetables"),
        "Фрукты": Category.objects.create(name="Фрукты", slug_name="fruits"),
        "Соки": Category.objects.create(name="Соки", slug_name="juices"),
        "Семена": Category.objects.create(name="Семена", slug_name="seeds")
    }

    # Создаём объект в таблице размерности
    UNIT = {
        "кг": Unit.objects.create(name="кг",
                                  description="Килограмм"),
        "л": Unit.objects.create(name="л",
                                 description="Килограмм")
    }

    # Создаём объект в таблице валюты
    CURRENCY = {
        "руб": Currency.objects.create(name="руб",
                                       description="Рубль")
    }

    PRODUCT = {}
    for product in DATABASE.values():
        product_obj = \
            Product.objects.create(name=product["name"],
                                   description=product["description"],
                                   slug_name=product["html"],
                                   unit=UNIT["кг"] if product["category"] != "Соки" else UNIT["л"],
                                   quantity_per_unit=1.0,
                                   price=product["price_before"],
                                   currency=CURRENCY["руб"],
                                   category=CATEGORY[product["category"]],
                                   )
        # Сейчас был создан продукт, но не была сохранена картинка. Если в поле
        # image вы храните только путь до картинки и её физически перемещать
        # не нужно в хранилище, то можно указать название картинки
        # в этом хранилище и возможное отклонение пути. Но у нас картинка
        # перемещается в наше хранилище по пути static/products,
        # поэтому будет нужно сделать следующие действия

        # Определим полный путь до картинки (соединим пути рабочей папки,
        # папок store, static и пути, что прописан в product["url"])
        path_pic = os.path.join(project_directory,
                                'store',
                                'static',
                                *product["url"].split("/"))
        # product["url"].split("/") делаем, чтобы избавиться от "/",
        # а os.path.join сам подставил нужный разделитель

        # Дальше откроем нашу картинку, создадим объект File
        # и в продукте в поле image сохранием этот файл
        with open(path_pic, 'rb') as image_file:
            image = File(image_file)
            basename = os.path.basename(image.name)  # Имя файла
            product_obj.image.save(basename, image)

        PRODUCT[product["name"]] = product_obj  # Сохраняем в словаре для
        # дальнейшего быстрого доступа, чтобы не обращаться в БД

    # Создаём вариацию продукта
    PRODUCT_VARIANT = {}
    for product in DATABASE.values():
        product_obj = ProductDetail.objects.create(
            product=PRODUCT[product["name"]],
            rating_mean=product["rating"],
            review_count=product["review"],
            sold_value=product["sold_value"],
            quantity_in_stock=product["weight_in_stock"],
        )

    print("___Продукты созданы___")

    DISCOUNTS = {}

    for product in DATABASE.values():
        if product['discount']:
            product_discount_obj = ProductDiscount.objects.create(
                product=PRODUCT[product["name"]],
                value=product['discount'],
                is_percentage=True,
                start_date=datetime(2023, month=12, day=1,
                                    hour=0, minute=0, second=0, tzinfo=timezone.utc),
                end_date=datetime(2024, month=12, day=1,
                                  hour=0, minute=0, second=0, tzinfo=timezone.utc),
            )

    print("___Скидки созданы___")
