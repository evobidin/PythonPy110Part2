from django.contrib import admin
from .models import ShippingAddress, Delivery

admin.site.register(ShippingAddress)
admin.site.register(Delivery)
