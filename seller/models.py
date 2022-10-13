from django.db import models


class SellerModel(models.Model):
    seller = models.CharField()
    