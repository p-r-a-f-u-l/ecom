from django.contrib import admin

from .models import Banner, FlashSale, FlashSaleProduct


admin.site.register(FlashSale)
admin.site.register(FlashSaleProduct)
admin.site.register(Banner)
