from math import trunc

from django.contrib.auth import get_user_model
from rest_framework import serializers

from products.models import ColorF, ImageBulk, Product, Review, SubBrand, Brand, SubDemo

User = get_user_model()


class CustomUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id", "email", "profile_dp"]


class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUser(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "star", "des", "user", "created_at")


class ProductColor(serializers.ModelSerializer):
    class Meta:
        model = ColorF
        fields = ("color",)


class BrandSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "company_name",
        ]


class ImageBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBulk
        fields = ("image",)


class ReviewProduct(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    product_image = ImageBulkSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "product_image",
            "reviews",
        ]


class ProductSerializer(serializers.ModelSerializer):
    product_cost = serializers.SerializerMethodField()
    product_discount = serializers.SerializerMethodField()
    product_color = ProductColor(many=True)
    reviews = ReviewSerializer(many=True)
    product_available = serializers.SerializerMethodField()
    product_image = ImageBulkSerializer(many=True)
    favourite = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    old_product_cost = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self, product):
        return product.sub_brand.brand_name

    def get_brand(self, product):
        request = self.context.get("request")
        return product.brand.company_name

    def get_favourite(self, product):
        request = self.context.get("request")
        if product.favourite.filter(id=request.user.id).exists():
            return True
        return False

    # def get_product_image(self, product):
    #     request = self.context.get("request")
    #     image = product.product_image.all()
    #     return request.build_absolute_uri(image)

    def get_product_discount(self, obj):
        if obj.product_discount == 0:
            return obj.product_discount
        else:
            return obj.product_discount

    def get_product_cost(self, obj):
        if obj.product_discount > 100:
            return "Free"
        elif obj.product_discount > 0:
            return trunc(
                obj.product_cost - (obj.product_cost * obj.product_discount) / 100
            )
        else:
            return obj.product_cost

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

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "product_image",
            "product_description",
            "product_color",
            "product_size",
            "product_quantity",
            "product_available",
            "product_cost",
            "product_discount",
            "old_product_cost",
            "product_rating",
            "product_created",
            "product_updated",
            "reviews",
            "favourite",
            "views",
            "brand",
            "category",
            "product_category",
        ]


class SubProductSerializer(serializers.ModelSerializer):
    product_cost = serializers.SerializerMethodField()
    product_discount = serializers.SerializerMethodField()
    product_color = ProductColor(many=True)
    reviews = ReviewSerializer(many=True)
    product_available = serializers.SerializerMethodField()
    product_image = ImageBulkSerializer(many=True)
    favourite = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    old_product_cost = serializers.SerializerMethodField()

    def get_brand(self, product):
        return product.brand.company_name

    def get_category(self, product):
        return product.sub_brand.brand_name

    def get_favourite(self, product):
        request = self.context.get("request")
        if product.favourite.filter(id=request.user.id).exists():
            return True
        return False

    def get_old_product_cost(self, obj):
        if obj.product_discount > 0:
            return obj.product_cost
        else:
            return 0

    def get_product_image(self, product):
        request = self.context.get("request")
        image = product.product_image.url
        return request.build_absolute_uri(image)

    def get_product_discount(self, obj):
        if obj.product_discount == 0:
            return obj.product_discount
        else:
            return obj.product_discount

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
            "product_description",
            "product_color",
            "product_size",
            "product_quantity",
            "product_available",
            "product_cost",
            "product_discount",
            "old_product_cost",
            "product_rating",
            "product_created",
            "product_updated",
            "reviews",
            "favourite",
            "brand",
            "category",
        ]


class CartProductSerializer(serializers.ModelSerializer):
    product_cost = serializers.SerializerMethodField()
    product_available = serializers.SerializerMethodField()
    product_discount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    product_color = ProductColor(many=True)
    reviews = ReviewSerializer(many=True)

    def get_total(self, obj):
        return ""

    def get_quantity(self, obj):
        return ""

    def get_product_discount(self, obj):
        if obj.product_discount == 0:
            return obj.product_discount
        else:
            return obj.product_discount

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
            "product_description",
            "product_color",
            "product_size",
            "product_available",
            "product_cost",
            "product_discount",
            "product_rating",
            "quantity",
            "total",
            "product_created",
            "product_updated",
            "reviews",
        ]


class SubBrandSerializer(serializers.ModelSerializer):
    subs = ProductSerializer(many=True, read_only=True)
    title = serializers.SerializerMethodField()

    def get_title(self, subbrand):
        return "SubBrand"

    class Meta:
        model = SubBrand
        fields = (
            "title",
            "id",
            "brand_name",
            "brand_image",
            "subs",
        )


class SUbDEMO(serializers.Serializer):
    subdemo = SubBrandSerializer(many=True, read_only=True)

    class Meta:
        model = SubDemo
        fields = ["id", "subdemo"]


class BrandSerializer(serializers.ModelSerializer):
    brands = SubBrandSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "company_name",
            "company_desc",
            "company_logo",
            "brands",
        ]


class CateSubBrandSerializer(serializers.ModelSerializer):
    subs = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubBrand
        fields = (
            "id",
            "brand_name",
            "brand_image",
            "subs",
        )


class CategorySerializer(serializers.ModelSerializer):
    brands = CateSubBrandSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "company_name",
            "company_desc",
            "company_logo",
            "brands",
        ]
