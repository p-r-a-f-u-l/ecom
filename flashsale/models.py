from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from ecom.validators import check_image
from products.models import ColorF

product_size = (
    ('small', 'small'),
    ('medium', 'medium'),
    ('large', 'large'),
    ('extra large', 'extra large'),
    ('extra extra large', 'extra extra large'),
)
Product_Category = (
    ('mobile', 'mobile'),
    ('tv', 'tv'),
    ('tablet', 'tablet'),
    ('laptop', 'laptop'),
)


class FlashSaleProduct(models.Model):
    product_name = models.CharField(max_length=120)
    product_category = models.CharField(
        choices=Product_Category, default='mobile', max_length=120)
    product_image = models.ImageField(
        upload_to='media/flashsale',
        validators=[check_image, FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'jpeg'])])
    product_description = models.TextField(max_length=500)
    product_color = models.ManyToManyField(ColorF)
    product_size = models.CharField(
        choices=product_size, blank=True, max_length=20)
    product_quantity = models.IntegerField()
    product_available = models.BooleanField(default=True)
    product_cost = models.BigIntegerField(blank=False)
    product_rating = models.FloatField(blank=True)
    product_discount = models.IntegerField()
    product_created = models.DateTimeField(auto_now_add=timezone.now)
    product_updated = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return self.product_name


class Banner(models.Model):
    banner = models.ImageField(
        upload_to='flashsale/banner',
        validators=[check_image, FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'jpeg'])])
    title = models.CharField(max_length=225, default='')

    def __str__(self) -> str:
        return self.title


class FlashSale(models.Model):
    flash = models.CharField(max_length=120, blank=False)
    banner = models.ManyToManyField(Banner)
    product = models.ManyToManyField(FlashSaleProduct)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.flash
