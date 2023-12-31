from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Cart(models.Model):
    """Модель корзины"""
    customer = models.OneToOneField(User,
                                    related_name='cart',
                                    on_delete=models.CASCADE)  # Ссылка на пользователя (у пользователя может быть только одна корзина)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"Корзина пользователя: {self.customer.username}"


class CartItem(models.Model):
    """Модель позиций в корзине"""
    cart = models.ForeignKey(Cart,
                             related_name='items',
                             on_delete=models.CASCADE)  # Ссылка на корзину
    product = models.ForeignKey(Product,
                                related_name='cart_items',
                                on_delete=models.CASCADE)  # Ссылка на продукт
    quantity = models.PositiveIntegerField(default=1)  # Число товаров в позиции заказа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
