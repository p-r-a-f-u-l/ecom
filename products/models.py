from uuid import uuid4

from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe

from ecom.validators import check_image

User = get_user_model()

product_color = (
    ("red", "red"),
    ("yellow", "yellow"),
    ("purple", "purple"),
    ("black", "black"),
    ("green", "green"),
    ("white", "white"),
)

product_size = (
    ("small", "small"),
    ("medium", "medium"),
    ("large", "large"),
    ("extra large", "extra large"),
    ("extra extra large", "extra extra large"),
)


class Brand(models.Model):
    company_name = models.CharField(max_length=120)
    company_desc = models.CharField(max_length=120)
    company_logo = models.ImageField(
        upload_to="media/brand",
        validators=[
            check_image,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "jpeg"]),
        ],
    )

    def image_show(self):
        if self.company_logo:
            return mark_safe(f"<img src={self.company_logo.url} width=50, height=50 />")
        else:
            return ""

    image_show.short_description = "company logo"

    def __str__(self):
        return self.company_name


class SubBrand(models.Model):
    brandname = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="brands"
    )
    brand_name = models.CharField(max_length=120)
    brand_image = models.ImageField(
        upload_to="media/subbrand",
        validators=[
            check_image,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "jpeg"]),
        ],
    )

    def __str__(self):
        return self.brand_name

    def image_show(self):
        if self.brand_image:
            return mark_safe(f"<img src={self.brand_image.url} width=50, height=50 />")
        else:
            return ""

    image_show.short_description = "brand image"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    star = models.FloatField(blank=False, null=False)
    des = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)


class ColorF(models.Model):
    name = models.CharField(max_length=40, blank=False)
    color = ColorField(default="#FF0000")

    def __str__(self):
        return self.name


Product_Category = (
    ("mobile", "mobile"),
    ("tv", "tv"),
    ("tablet", "tablet"),
    ("laptop", "laptop"),
)


class ImageBulk(models.Model):
    image = models.ImageField(
        upload_to="media/product",
        validators=[
            check_image,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "jpeg"]),
        ],
    )

    def __str__(self) -> str:
        return str(self.image)


class Product(models.Model):
    sub_brand = models.ForeignKey(
        SubBrand, on_delete=models.CASCADE, related_name="subs"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="brandsname"
    )
    product_name = models.CharField(max_length=120)
    product_category = models.CharField(
        choices=Product_Category, default="mobile", max_length=120
    )
    product_image = models.ManyToManyField(ImageBulk)
    product_description = models.TextField(max_length=500)
    product_color = models.ManyToManyField(ColorF)
    product_size = models.CharField(choices=product_size, blank=True, max_length=20)
    product_quantity = models.IntegerField()
    product_available = models.BooleanField(default=True)
    product_cost = models.BigIntegerField(blank=False)
    product_rating = models.FloatField(blank=True)
    product_discount = models.IntegerField()
    product_created = models.DateTimeField(auto_now_add=timezone.now)
    product_updated = models.DateTimeField(auto_now=timezone.now)
    is_fav = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    favourite = models.ManyToManyField(User, related_name="post_favourite", blank=True)
    reviews = models.ManyToManyField(
        Review,
        blank=True,
        related_name="review",
    )

    def image_show(self):
        if self.product_image:
            return mark_safe(
                f"<img src={self.product_image.url} width=50, height=50 />"
            )
        else:
            return ""

    image_show.short_description = "Item"

    def __str__(self):
        return self.product_name


class SubDemo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    product = models.ForeignKey(
        SubBrand, on_delete=models.CASCADE, related_name="subdemo"
    )
