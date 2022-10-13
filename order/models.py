from uuid import uuid1

from django.contrib.auth import get_user_model
from django.db import models

from users.models import CartDetails

User = get_user_model()

STATUS = (
    ('delivered', 'delivered'),
    ('processing', 'processing'),
    ('canceled', 'canceled'),
)

Order_Status = (
    ('Order Confirmed', 'order confirmed'),
    ('Order Processed', 'order Proccessed'),
    ('Order On The Way', 'order on the way'),
    ('Order Delivered', 'order delivered'),
)


class OrderStatus(models.Model):
    order_st = models.CharField(choices=Order_Status, max_length=40)
    comment = models.CharField(max_length=120, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class OrderID(models.Model):
    stripe_id = models.CharField(max_length=225, blank=False)
    status = models.CharField(max_length=12, blank=False)
#    cart_id = models.ForeignKey(CartDetails, on_delete=models.CASCADE)
    address_id = models.CharField(max_length=255, blank=False)
    phone_no = models.CharField(max_length=20, blank=False)
    quantity = models.CharField(max_length=8, blank=False)
    amount = models.CharField(max_length=20, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.stripe_id)


class Order(models.Model):
    order_uid = models.UUIDField(default=uuid1)
    order_info = models.ForeignKey(OrderID, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    total_amount = models.PositiveBigIntegerField(default=0)
    order_status = models.CharField(
        max_length=40, choices=STATUS, default='processing')
    order_comnt = models.ManyToManyField(OrderStatus, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.order_uid)
