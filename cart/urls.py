# urls.py in store

from django.urls import path
from .views import cart_view, cart_add_view, cart_del_view, cart_buy_now_view, cart_remove_view

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name="cart_view"),
    path('add/<str:id_product>', cart_add_view),
    path('del/<str:id_product>', cart_del_view),
    path('buy/<str:id_product>', cart_buy_now_view, name="buy_now"),
    path('remove/<str:id_product>', cart_remove_view, name="remove_now"),
]