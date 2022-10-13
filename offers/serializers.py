from rest_framework import serializers
from .models import OfferModel, OfferDis, OfferPoint, OfferEx, Description


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ("description",)


class OfferPointSerializer(serializers.ModelSerializer):
    points = DescriptionSerializer(many=True)

    class Meta:
        model = OfferPoint
        fields = ("op_title", "points")


class OfferExSerializer(serializers.ModelSerializer):
    ex_dis = OfferPointSerializer(many=True)

    class Meta:
        model = OfferEx
        fields = ("ex_title", "ex_dis")


class OfferDisSerialzier(serializers.ModelSerializer):
    offerex = OfferExSerializer(many=True)

    class Meta:
        model = OfferDis
        fields = ("title", "offerex")


class OfferModelSerializer(serializers.ModelSerializer):
    orderitems = OfferDisSerialzier(many=True)

    class Meta:
        model = OfferModel
        fields = ("offerTitle", "orderitems")
