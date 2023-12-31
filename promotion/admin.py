from django.contrib import admin
from .models import Promotion, Discount, FreeShipping, BuyGet

admin.site.register(Promotion)
admin.site.register(Discount)
admin.site.register(FreeShipping)
admin.site.register(BuyGet)