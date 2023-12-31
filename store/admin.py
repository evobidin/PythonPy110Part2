from django.contrib import admin
from django.apps import apps
from .models import Product, ProductDetail, Unit, Currency, Category, Review, ProductDiscount

app = apps.get_app_config('store')
app.verbose_name = 'Магазин'  # verbose_name - заменит отображаемое название приложения в админ панели

admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductDiscount)
admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Review)
