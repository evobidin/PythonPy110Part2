from django.db import models


class Promotion(models.Model):
    """Модель промоакция"""
    name = models.CharField(max_length=255)  # Название промокции
    code = models.CharField(max_length=20,
                            unique=True)  # Уникальный код промокции
    description = models.TextField()  # Описание промокции
    start_date = models.DateTimeField()  # Дата и время начала промокции
    end_date = models.DateTimeField()  # Дата и время окончания промокции
    is_active = models.BooleanField(default=True)  # Флаг активности промокции
    created_at = models.DateTimeField(
        auto_now_add=True)  # Дата и время создания объекта сущности в базе данных
    updated_at = models.DateTimeField(
        auto_now=True)  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.name


class Discount(models.Model):
    """Модель Общая скидка на полную стоимость"""
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    is_percentage = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.value}{'%' if self.is_percentage else ''} скидки"


class FreeShipping(models.Model):
    """Модель Промокод на бесплатную доставку"""
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)

    def __str__(self):
        return "Бесплатная доставка"


class BuyGet(models.Model):
    """Промокод вида купи N товаров, а K получи бесплатно"""
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    buy_quantity = models.PositiveIntegerField()
    get_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Купи {self.buy_quantity}, Заплати за {self.get_quantity}"
