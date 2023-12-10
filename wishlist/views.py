from django.shortcuts import render, redirect
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from store.models import DATABASE
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse


@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request).get(current_user)

        products = []  # Список продуктов
        for product_id in data['products']:
            product = DATABASE.get(product_id)
            products.append(product)

        return render(request, 'wishlist/wishlist.html', context={"products": products})


def wishlist_add_json(request, id_product):
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в избранное"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_del_json(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_json(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request).get(current_user)
        if data:
            return JsonResponse(data,
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({"answer": "Пользователь не авторизирован"},
                            json_dumps_params={'ensure_ascii': False},
                            status=404)


def wishlist_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return redirect("wishlist:wishlist_view")

        return HttpResponse("Неудачное удаление из корзины", status=404)
