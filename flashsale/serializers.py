from rest_framework import serializers

from products.serializes import ProductColor
from .models import Banner, FlashSaleProduct, FlashSale


class BannerSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    def get_banner(self, banner):
        request = self.context.get('request')
        image = banner.banner.url
        return request.build_absolute_uri(image)

    class Meta:
        model = Banner
        fields = "__all__"


class FlashSaleSerializer(serializers.ModelSerializer):
    product_color = ProductColor(many=True)

    class Meta:
        model = FlashSaleProduct
        fields = (
            'id',
            "product_name",
            "product_category",
            "product_image",
            "product_description",
            "product_color",
            "product_size",
            "product_quantity",
            "product_available",
            "product_cost",
            "product_rating",
            "product_discount",
            "product_created",
            "product_updated",
        )


class FlashSerializer(serializers.ModelSerializer):
    product = FlashSaleSerializer(many=True)
    banner = BannerSerializer(many=True)

    class Meta:
        model = FlashSale
        fields = "__all__"
