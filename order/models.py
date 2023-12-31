from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    """Модель заказа"""
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)  # Ссылка на пользователя
    status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)  # Ссылка на статус заказа
    sum_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Общая цена продуктов
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"Заказ: {self.id}; Пользователь: {self.customer.username}; Статус: {self.status.name}"


class OrderItem(models.Model):
    """Модель позиций в заказе"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Ссылка на заказ
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)  # Ссылка на продукт
    quantity = models.PositiveIntegerField(default=1)  # Число товара в заказе
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class OrderStatus(models.Model):
    """Модель статусов заказа"""
    name = models.CharField(max_length=50)  # Обозначение статуса
    description = models.TextField(null=True)  # Описание статуса

    def __str__(self):
        return self.name
