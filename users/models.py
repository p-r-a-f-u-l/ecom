from uuid import uuid1

from django.conf import settings
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from products.models import Product

address_choice = (
    ('Home', "Home"),
    ("Work", 'Office'),
    ("Others", "Others"),
)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be contains only digits. Also Up to 10 digits allowed.")
    phone_number = models.CharField(
        _('phone no.'), max_length=10, blank=False, unique=False, validators=[phone_regex])
    #phone_number = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=150, blank=False, null=False)
    pincode = models.CharField(max_length=20, blank=False, null=False)
    country = CountryField()
    city = models.CharField(max_length=20, blank=False, null=False)
    district = models.CharField(max_length=70, blank=False, null=False)
    address_of = models.CharField(
        choices=address_choice, default='Home', max_length=20)
    created_on = models.DateTimeField(auto_now=timezone.now)
    updated_on = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


class CardDetails(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False,
                              editable=False)
    card_number = models.BigIntegerField(blank=False, null=False)
    holder_name = models.CharField(max_length=120, blank=False, null=False)
    expire_date = models.CharField(max_length=8, blank=False, null=False)
    created_on = models.DateTimeField(auto_now=timezone.now)
    updated_on = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.holder_name


class FavDetails(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=timezone.now)


class CartDetails(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=timezone.now)


PAYMENT_STATUS = (
    ('SUCCESS', 'S'),
    ('FAILED', 'F')
)


class Payment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False,
                              editable=False)
    payment_code = models.CharField(max_length=255, blank=False)
    payment_status = models.CharField(
        choices=PAYMENT_STATUS, default='F', max_length=20, blank=False)
    payment_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_status


class MasterCart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    mcart_id = models.UUIDField(default=uuid1)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(CartDetails)

    def __str__(self):
        return str(self.mcart_id)
