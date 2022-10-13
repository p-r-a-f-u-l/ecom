from django.contrib import admin
from .models import ImageBulk, Product, SubBrand, Brand, Review, ColorF

admin.site.register(Review)
admin.site.register(ColorF)
admin.site.register(ImageBulk)


@admin.register(Product)
class ProductConfig(admin.ModelAdmin):
    list_display = [
        "product_name",
        "product_description",
        "product_size",
        "product_quantity",
        "product_available",
        "product_cost",
        "product_discount",
        "product_created",
        "product_updated",
    ]
    list_per_page = 10
    list_filter = ["product_name"]
    readonly_fields = ("image_show",)


@admin.register(SubBrand)
class SubBrandConfig(admin.ModelAdmin):
    list_display = [
        "brand_name",
        "brand_image",
    ]
    list_per_page = 10
    list_filter = ["brand_name"]
    readonly_fields = ("image_show",)


@admin.register(Brand)
class BrandConfig(admin.ModelAdmin):
    list_display = [
        "company_name",
        "company_desc",
        "company_logo",
    ]
    list_per_page = 10
    list_filter = ["company_name"]
    readonly_fields = ("image_show",)
