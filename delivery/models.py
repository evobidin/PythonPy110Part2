from django.db import models
from django.contrib.auth.models import User
from order.models import Order

class ShippingAddress(models.Model):
    """Модель адреса доставки"""
    customer = models.ForeignKey(User, related_name='shipping_addresses', on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.country}"


class Delivery(models.Model):
    """Модель доставки"""
    order = models.OneToOneField(Order, related_name='delivery', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20, choices=[('В ожидании', 'В ожидании'),
                                                               ('Отправлено', 'Отправлено'),
                                                               ('Доставлено', 'Доставлено')])
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    estimated_delivery_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Доставка для заказа {self.order.id}, Статус: {self.delivery_status}"
