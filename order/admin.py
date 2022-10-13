from django.contrib import admin

from users.models import MasterCart
from .models import Order, OrderID, OrderStatus

admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(OrderID)
admin.site.register(MasterCart)
