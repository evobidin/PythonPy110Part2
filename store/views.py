from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from .models import Product
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def products_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            # Получение продукта по полю slug_name.
            product = Product.objects.filter(slug_name=page)
            # Создание запроса с дополнительными полями
            # (поля сделаны так, чтобы минимизировать изменения в коде product.html)
            product = product.annotate(
                price_before=F("price"),
                price_after=F("price_before") * (
                            100 - F("discount__value")) / 100,
                review=F("details__review_count"),
                rating=F("details__rating_mean"),
                sold_value=F("details__sold_value"),
                weight_in_stock=F("details__quantity_in_stock"),
            )
            product = product.first()  # Получение первого элемента из QuerySet

            return render(request, "store/product.html",
                          context={"product": product})

        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id

            # Можно сделать и одни запросом при помощи метода get. Метод get возвращает только один объект, всегда.
            # get не возвращает QuerySet, поэтому после get нельзя делать аннотации, фильтры, и т.д.

            product = Product.objects.annotate(
                price_before=F("price"),
                price_after=F("price_before") * (
                        100 - F("discount__value")) / 100,
                review=F("details__review_count"),
                rating=F("details__rating_mean"),
                sold_value=F("details__sold_value"),
                weight_in_stock=F("details__quantity_in_stock"),
            ).get(id=page)

            return render(request, "store/product.html",
                          context={"product": product})

        return HttpResponse(status=404)


# def products_page_view(request, page):  # для решения последней доп. задачи
#     limit = 5
#     if request.method == "GET":
#         if isinstance(page, str):
#             for data in DATABASE.values():
#                 if data['html'] == page:
#                     data_category = filter(
#                         lambda x: x["id"] != data['id'],
#                         filtering_category(DATABASE, data['category']))
#                     return render(request, "store/product.html", context={"product": data,
#                                                                           "products_category": list(data_category)[
#                                                                                                :limit]})
#
#         elif isinstance(page, int):
#             # Обрабатываем условие того, что пытаемся получить страницу товара по его id
#             data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
#             if data:
#                 data_category = filter(
#                     lambda x: x["id"] != data['id'],
#                     filtering_category(DATABASE, data['category']))
#                 return render(request, "store/product.html",
#                               context={"product": data,
#                                        "products_category": list(data_category)[:limit]})
#
#         return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        products = Product.objects.all().annotate(
            price_before=F("price"),
            price_after=F("price_before")*(100-F("discount__value"))/100
        )
        # Обработка фильтрации из параметров запроса
        if category_key := request.GET.get("category"):  # Если существует category в адресной строке
            if ordering_key := request.GET.get("ordering"):   # Если существует ordering в адресной строке
                if request.GET.get("reverse") in ('true', 'True'):
                    data = products.filter(category__name=category_key).order_by(f"-{ordering_key}")
                else:
                    data = products.filter(category__name=category_key).order_by(ordering_key)
            else:
                data = products.filter(category__name=category_key)
        else:
            data = products

        # # Добавляем пагинацию
        # page = request.GET.get('page', 1)
        # paginator = Paginator(data, 5)  # Разбиваем на 5 элементов на странице
        # try:
        #     data = paginator.page(page)
        # except PageNotAnInteger:
        #     data = paginator.page(1)
        # except EmptyPage:
        #     data = paginator.page(paginator.num_pages)
        #
        return render(request, 'store/shop.html',
                      context={"products": data,
                               "category": category_key})


def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        # Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)

        # Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")
        if name_coupon in DATA_COUPON:
            coupon = DATA_COUPON[name_coupon]
            return JsonResponse({"discount": coupon["value"], "is_valid": coupon["is_valid"]})
        return HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        if country := DATA_PRICE.get(data.get('country')):
            if city := country.get(data.get('city')):
                return JsonResponse({"price": city["price"]})
            return JsonResponse({"price": country["fix_price"]})
        return HttpResponseNotFound("Неверные данные")
