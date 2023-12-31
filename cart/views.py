from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from store.models import DATABASE
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product
from django.db.models import ExpressionWrapper, F, DecimalField, Case, When, Value



@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == "GET":
        cart = Cart.objects.get(customer=request.user)

        # При помощи select_related подгружаем дополнительные таблицы в одном запросе,
        # чтобы уменьшить число запросов
        products = cart.items.select_related(
            'product',
            'product__discount',
            'product__image').all()  # Список продуктов
        # Проводим аннотацию, чтобы собрать нужные значения в products
        products = products.annotate(
            price_after=Case(
                When(product__discount__isnull=False,
                     then=ExpressionWrapper(
                         F("product__price") * (100 - F(
                             "product__discount__value")) / 100,
                         output_field=DecimalField()
                     )),
                default=F("product__price"),  # Если скидки нет, использовать обычную цену
            ),  # Case - оператор выбора при условии When, если нет подходящих условий,
            # то возвращается default
            price_total=ExpressionWrapper(
                F("quantity") * F("price_after"),
                output_field=DecimalField()),
            name=F("product__name"),
            description=F("product__description"),
            url=F("product__image"),
        ).values("id", "quantity", "price_after", "price_total", "name", "description", "url")
        # values аналогично SELECT позволяет в запросе указать на вывод только те колонки, что необходимы
        return render(request, "cart/cart.html", context={"products": products})


@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        cart = Cart.objects.get(customer=request.user)  # Получили корзину по пользователю
        product = Product.objects.get(id=id_product)  # Получили продукт по его id
        products_cart = cart.items.filter(product=product)
        if products_cart:
            cart_item = products_cart.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product)  # Создали объект в CartItem по данным
        return redirect("cart:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")


def cart_remove_view(request, id_product):
    # id_product - неудачное название, так как на самом деле передаётся id_cart_item
    # тоесть номер строки в базе данных CartItem, поэтому при удалении получаем объект по его id и удаляем
    if request.method == "GET":
        cart_item = CartItem.objects.get(id=id_product)  # получаем объект по его id
        if cart_item:
            cart_item.delete()  # удаляем объект из БД
            return redirect("cart:cart_view")
        return HttpResponseNotFound("Неудачное удаление из корзины")


@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    # Реализация для добавления в корзину, при нажатии на + на главной странице
    # (когда возвращается JSON, а не html)
    if request.method == "GET":
        cart = Cart.objects.get(customer=request.user)
        product = Product.objects.get(id=id_product)
        products_cart = cart.items.filter(product=product)
        if products_cart:
            cart_item = products_cart.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product)  # Создали объект в CartItem по данным
        return JsonResponse(
            {"answer": "Продукт успешно добавлен в корзину"},
            json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    def cart_del_view(request, id_product):
        # Реализация для удаления из корзины с возвращением JSON, а не html
        if request.method == "GET":
            cart_item = CartItem.objects.get(id=id_product)
            if cart_item:
                cart_item.delete()
                return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                    json_dumps_params={'ensure_ascii': False})

            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})