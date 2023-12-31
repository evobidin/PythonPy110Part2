# urls.py in store

from django.urls import path
from .views import products_view, shop_view, products_page_view, coupon_check_view, delivery_estimate_view

app_name = 'store'

urlpatterns = [
    path('product/', products_view),
    path('', shop_view, name="shop_view"),
    path('product/<slug:page>.html', products_page_view, name="products_page_view"),
    path('product/<int:page>', products_page_view),

    path('coupon/check/<slug:name_coupon>', coupon_check_view),
    path('delivery/estimate/', delivery_estimate_view),
]