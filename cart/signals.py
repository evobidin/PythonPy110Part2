from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart


# Принимается сигнал post_save отправленный от модели User(сигнал post_save
# отправляется после того, как объект модели (в конкретном случае
# User (пользователь)) был создан в базе данных)
@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Создание корзины при создании пользователя"""
    if created:  # Значение True говорит о том, что объект(instance) был создан, а не идёт его обновление
        Cart.objects.create(
            customer=instance)  # Создаём корзину для пользователя

"""Код ниже не нужно раскомментировать, он показывает как можно удалить корзину, 
при удалении пользователя, но нам это не требуется, так как в модели Cart у 
поля customer в отношениях у нас стоит on_delete=models.CASCADE который на уровне
базы данных удалит строку в корзине при удалении пользователя из БД."""
"""
@receiver(post_delete, sender=User)
def delete_user_cart(sender, instance, **kwargs):
    try:
        cart = Cart.objects.get(customer=instance)
        cart.delete()
    except Cart.DoesNotExist:
        pass
"""
