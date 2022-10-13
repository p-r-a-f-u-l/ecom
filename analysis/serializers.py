from math import trunc
from rest_framework import serializers

from .models import AnalysisProduct, RecentProduct

from products.models import Product
from products.serializes import ImageBulkSerializer


class AnalysisProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisProduct
        fields = (
            "product_id",
            "count",
        )


class ProductShortCutSerializer(serializers.ModelSerializer):
    product_discount = serializers.SerializerMethodField()
    product_available = serializers.SerializerMethodField()
    product_image = ImageBulkSerializer(many=True)
    old_product_cost = serializers.SerializerMethodField()

    def get_product_discount(self, obj):
        if obj.product_discount == 0:
            return obj.product_discount
        else:
            return obj.product_discount

    def get_old_product_cost(self, obj):
        if obj.product_discount > 0:
            return obj.product_cost
        else:
            return 0

    def get_product_available(self, obj):
        if obj.product_quantity == 0:
            return "Sold Out"
        elif obj.product_quantity < 6:
            return f"Only {obj.product_quantity} Left"
        else:
            return "Available"

    def get_product_cost(self, obj):
        if obj.product_discount > 100:
            return "Free"
        elif obj.product_discount > 0:
            return trunc(
                obj.product_cost - (obj.product_cost * obj.product_discount) / 100
            )
        else:
            return obj.product_cost

    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "product_image",
            "product_description",
            "product_available",
            "product_cost",
            "product_discount",
            "old_product_cost",
            "product_rating",
            "product_created",
            "product_updated",
        )


class RecentlyProductSerializer(serializers.ModelSerializer):
    product_no = ProductShortCutSerializer()

    class Meta:
        model = RecentProduct
        fields = ["product_no", "owner", "create_at"]
