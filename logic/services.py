import json
import os
from store.models import DATABASE
from django.contrib.auth import get_user


def filtering_category(database: dict,
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False,
                       ):
    """
    Функция фильтрации данных по параметрам.

    :param database: База данных.
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список.
    """
    if category_key is not None:
        result = [value for value in database.values() if value['category'] == category_key]
    else:
        result = [*database.values()]
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)
    return result


def view_in_cart(request) -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username  # Получаем авторизированного пользователя
    cart = {user: {'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product not in cart['products']:
        if not DATABASE.get(id_product):
            return False
        cart['products'][id_product] = 1
    else:
        cart['products'][id_product] += 1
    # Если товар существует, то увеличиваем его количество на 1

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True


def remove_from_cart(request, id_product: str) -> bool:
    """
    Удаляем позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product not in cart['products']:
        return False

    cart['products'].pop(id_product)  # Если существует, то удаляем ключ 'id_product' у cart['products'].

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True


def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)

    cart = cart_users.get(username)

    if not cart:
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)


def view_in_wishlist(request) -> dict:
    """
    Просматривает содержимое wishlist.json

    :return: Содержимое 'wishlist.json'
    """
    if os.path.exists('wishlist.json'):  # Если файл существует
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username
    wishlist = {user: {'products': []}}  # Создаём пустую корзину
    with open('wishlist.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(wishlist, f)

    return wishlist


def add_to_wishlist(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if id_product not in wishlist['products']:
        if not DATABASE.get(id_product):
            return False
        wishlist['products'].append(id_product)
    else:
        return False

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True


def remove_from_wishlist(request, id_product: str) -> bool:
    """
    Удаляем позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if id_product not in wishlist['products']:
        return False

    wishlist['products'].remove(id_product)  # Если существует, то удаляем ключ 'id_product' у cart['products'].

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True


def add_user_to_wishlist(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных избранное, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    wishlist_users = view_in_wishlist(request)

    wishlist = wishlist_users.get(username)

    if not wishlist:
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products': []}
            json.dump(wishlist_users, f)


if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    print(view_in_cart())  # {'products': {}}
    print(add_to_cart('1'))  # True
    print(add_to_cart('0'))  # False
    print(add_to_cart('1'))  # True
    print(add_to_cart('2'))  # True
    print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
    print(remove_from_cart('0'))  # False
    print(remove_from_cart('1'))  # True
    print(view_in_cart())  # {'products': {'2': 1}}

    # from store.models import DATABASE
    #
    # test = [
    #     {'name': 'Клубника', 'discount': None, 'price_before': 500.0, 'price_after': 500.0,
    #      'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
    #      'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg', 'html': 'strawberry'
    #      },
    #
    #     {'name': 'Яблоки', 'discount': None, 'price_before': 130.0, 'price_after': 130.0,
    #      'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
    #      'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg', 'html': 'apple'
    #      }
    # ]
    #
    # print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True
