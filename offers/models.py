from django.db import models


class Description(models.Model):
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description[:10]


class OfferPoint(models.Model):
    op_title = models.CharField(max_length=20, blank=True)
    points = models.ManyToManyField(Description)

    def __str__(self):
        return self.op_title


class OfferEx(models.Model):
    ex_title = models.CharField(max_length=80, blank=False)
    ex_dis = models.ManyToManyField(OfferPoint)

    def __str__(self):
        return self.ex_title


class OfferDis(models.Model):
    title = models.CharField(blank=False, max_length=200)
    offerex = models.ManyToManyField(OfferEx)

    def __str__(self):
        return self.title


class OfferModel(models.Model):
    offerTitle = models.CharField(blank=False, max_length=40)
    orderitems = models.ManyToManyField(OfferDis)

    def __str__(self):
        return self.offerTitle
