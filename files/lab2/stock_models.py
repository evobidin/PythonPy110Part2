from django.db import models
from store.models import Product


class Warehouse(models.Model):
    """Модель складов"""
    name = models.CharField(max_length=255)  # Имя склада
    location = models.CharField(max_length=255)  # Адрес, где находится
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.name


class WarehouseItem(models.Model):
    """Объект склада"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # Ссылка на склад
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Ссылка на продукт
    quantity = models.PositiveIntegerField(default=0)  # Количество продукта на складе
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"{self.product.name} ({self.quantity} {self.product.unit.name})"
