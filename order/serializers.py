from rest_framework import serializers

from users.serializers import CartSerializer
from .models import Order, OrderID, OrderStatus


class OrderInfoSerializers(serializers.ModelSerializer):
    #cart_id = CartSerializer(many=True)

    class Meta:
        model = OrderID
        fields = (
            "address_id",
            "phone_no",
           # "cart_id",
        )


class OrderStatusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    order_comnt = OrderStatusInfoSerializer(many=True)
    order_info = OrderInfoSerializers()

    class Meta:
        model = Order
        fields = (
            "id",
            "order_info",
            "order_comnt",
            "order_uid",
            "quantity",
            "total_amount",
            "order_status",
            "created_at",
            "updated_at",
            "user",
        )


# (3, 94396b18-c7ad-11ec-9a9b-a1b1608c7cee, 0, 0, processing, 2022-04-29 11: 14: 47.171011+00, 2022-04-29 11: 14: 47.171033+00, null, 1).

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_status',)


class OrderIdSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
#    cart_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderID
        fields = (
            "stripe_id",
 #           "cart_id",
            "address_id",
            "phone_no",
            "status",
            "owner",
            "quantity",
            "amount",
        )
