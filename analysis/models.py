from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product


User = get_user_model()


class AnalysisProduct(models.Model):
    product_id = models.PositiveIntegerField(default=0, unique=True)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product_id, self.count


class RecentProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_no = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.owner, self.product_no)
