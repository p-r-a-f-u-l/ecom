from math import trunc

from rest_framework import serializers

from products.models import Product
from products.serializes import ProductSerializer, ImageBulkSerializer
from .models import Address, CardDetails, FavDetails, CartDetails, Payment, MasterCart


class CardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = [
            "id",
            "card_number",
            "holder_name",
            "expire_date",
        ]


class AddressInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "name",
            "phone_number",
            "address",
            "pincode",
            "country",
            "city",
            "district",
            "address_of",
        )


class FavItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = FavDetails
        fields = "__all__"


class AddFavItemSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FavDetails
        fields = (
            "owner",
            "product",
        )


class CartShortProductSerializer(serializers.ModelSerializer):
    product_cost = serializers.SerializerMethodField()
    product_available = serializers.SerializerMethodField()
    product_image = ImageBulkSerializer(many=True)

    # def get_product_image(self, product):
    #     request = self.context.get("request")
    #     image = product.product_image.url
    #     return request.build_absolute_uri(image)

    def get_product_cost(self, obj):
        if obj.product_discount > 100:
            return "Free"
        elif obj.product_discount > 0:
            return trunc(
                obj.product_cost - (obj.product_cost * obj.product_discount) / 100
            )
        else:
            return obj.product_cost

    def get_product_available(self, obj):
        if obj.product_quantity == 0:
            return "Sold Out"
        elif obj.product_quantity < 6:
            return f"Only {obj.product_quantity} Left"
        else:
            return "Available"

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "product_image",
            "product_available",
            "product_cost",
            "product_created",
            "product_updated",
        ]


class CartSerializer(serializers.ModelSerializer):
    product = CartShortProductSerializer(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return obj.quantity * obj.product.product_cost

    class Meta:
        model = CartDetails
        fields = (
            "id",
            "product",
            "owner",
            "quantity",
            "price",
            "created_on",
        )


class AddCartSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartDetails
        fields = ("owner", "product", "quantity")


class PaymentInfoSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "owner",
            "payment_code",
        )


class MasterCartSerializer(serializers.ModelSerializer):
    mcart_id = serializers.UUIDField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.SerializerMethodField()
    subprice = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    products = CartSerializer(many=True)

    def get_price(self, obj):
        return sum(
            [item.product.product_cost * item.quantity for item in obj.products.all()]
        )

    def get_quantity(self, obj):
        return sum([item.quantity for item in obj.products.all()])

    def get_subprice(self, obj):
        price = self.get_price(obj)
        return int(price * 12 / 100) + price

    class Meta:
        model = MasterCart
        fields = "__all__"
