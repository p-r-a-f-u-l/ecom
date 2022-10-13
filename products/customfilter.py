from django_filters import FilterSet, NumberFilter, CharFilter

from .models import Product, Brand


class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name='product_cost', lookup_expr='gte')
    max_price = NumberFilter(field_name='product_cost', lookup_expr='lte')
    max_rating = NumberFilter(field_name='product_rating', lookup_expr='lte')
    min_rating = NumberFilter(field_name='product_rating', lookup_expr='gte')
    brand_search = CharFilter(
        field_name='brand__company_name', lookup_expr='istartswith')
    sub_search = CharFilter(
        field_name="sub_brand__brand_name", lookup_expr="istartswith"
    )

    class Meta:
        model = Product
        fields = ('max_price',
                  'min_price',
                  'max_rating',
                  'min_rating',
                  'brand_search',
                  'sub_search',
                  )


class BrandFilter(FilterSet):
    min_price = NumberFilter(
        field_name='brands__product_cost', lookup_expr='gte')
    max_price = NumberFilter(
        field_name='brands__product_cost', lookup_expr='lte')
    max_rating = NumberFilter(
        field_name='brands__product_rating', lookup_expr='lte')
    min_rating = NumberFilter(
        field_name='brands__product_rating', lookup_expr='gte')
    product_search = CharFilter(field_name='brands__product_name')
    brand_search = CharFilter(field_name='company_name')

    class Meta:
        model = Brand
        fields = ('max_price',
                  'min_price',
                  'max_rating',
                  'min_rating',
                  'product_search',
                  'brand_search',
                  )
