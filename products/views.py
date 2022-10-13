from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.serializers import CartSerializer

from .customfilter import ProductFilter, BrandFilter
from .models import Product, Brand, SubBrand, Review
from .serializes import (
    CartProductSerializer,
    CategorySerializer,
    ProductSerializer,
    BrandSerializer,
    ReviewProduct,
    ReviewSerializer,
    SubBrandSerializer,
    SubProductSerializer,
)

from users.models import CartDetails

User = get_user_model()


class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "message": args.get("message", "success"),
            "error": args.get(
                "error",
            ),
            "data": args.get("data", []),
        }


class TopRating(ModelViewSet):
    queryset = Product.objects.filter(product_rating__gte=3.0)
    serializer_class = ProductSerializer
    http_method_names = ("get",)


class ReviewInfo(APIView):
    def get(self, request):
        query = Product.objects.filter(reviews__user__id=request.user.id).all()
        serializer = ReviewProduct(query, many=True)
        return Response(data=serializer.data)


class ReviewIndex(APIView):
    bad_request_message = "An error has occurred"

    def get(self, request, pk):
        post = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(post, context={"request": request})
        if request.user in post.reviews.all():
            return Response({"data": serializer.data})
        return Response({"data": serializer.data})

    def post(self, request, pk):
        post = get_object_or_404(Product, pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if not post.reviews.filter(user_id=request.user.id).exists():
            serializer.is_valid()
            serializer.save(user=request.user)
            # post.reviews.add(request.data)
            ids = serializer.data.get("id")
            post.reviews.add(ids)

            return Response({"detail": "Added."}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "You can't Review Again."}, status=status.HTTP_400_BAD_REQUEST
        )

    # def delete(self, request, pk):
    #     print(request, pk)
    #     post = get_object_or_404(Product, pk=pk)
    #     if request.user in post.reviews.all():
    #         post.reviews.remove(request.user)
    #         return Response({'detail': 'Favorite Removed'}, status=status.HTTP_204_NO_CONTENT)
    #     return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


class IndexID(APIView):
    bad_request_message = "An error has occurred"

    def get(self, request, pk):
        post = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(post, context={"request": request})
        card = CartDetails.objects.filter(owner_id=request.user.id).filter(
            product__id=pk
        )
        cartSerializer = CartSerializer(card, many=True, context={"request": request})
        if cartSerializer.data:
            data = {"data": serializer.data, "inCart": True}
            return Response(data=data, status=status.HTTP_200_OK)
        data = {"data": serializer.data, "inCart": False}
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Product, pk=pk)
        if not post.favourite.filter(id=request.user.id).exists():
            post.favourite.add(request.user)
            Product.objects.filter(pk=pk).update(is_fav=True)
            return Response({"detail": "Favorite Added"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "You can't Favorite One Item Twice Time"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        post = get_object_or_404(Product, pk=pk)
        if post.favourite.filter(id=request.user.id).exists():
            post.favourite.remove(request.user)
            # Product.objects.filter().update(is_fav=False)
            return Response(
                {"detail": "Favorite Removed"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST
        )


class Index(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(Index, self).__init__(**kwargs)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    )
    search_fields = (
        "product_name",
        "product_category",
    )
    filter_class = ProductFilter
    ordering_fields = ("product_rating", "product_cost", "product_created")
    http_method_names = ("get",)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response_data = super(Index, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class SubbrandIndex(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SubbrandIndex, self).__init__(**kwargs)

    queryset = Product.objects.all()
    serializer_class = SubProductSerializer
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    )
    search_fields = (
        "product_name",
        "product_category",
    )
    filter_class = ProductFilter
    ordering_fields = ("product_rating", "product_cost", "product_created")
    http_method_names = ("get",)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response_data = super(SubbrandIndex, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class SubBrandIndex(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SubBrandIndex, self).__init__(**kwargs)

    queryset = SubBrand.objects.all()
    serializer_class = SubBrandSerializer
    http_method_names = ("get",)
    filter_backends = [SearchFilter]
    search_fields = ["brand_name"]

    def list(self, request, *args, **kwargs):
        response_data = super(SubBrandIndex, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class BrandIndex(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(BrandIndex, self).__init__(**kwargs)

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # filter_backends = (SearchFilter,)
    filter_class = BrandFilter
    http_method_names = ("get",)

    def list(self, request, *args, **kwargs):
        response_datas = super(BrandIndex, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_datas.data
        if not response_datas.data:
            self.response_format["message"] = "NO Data Found."
            self.response_format["error"] = response_datas.status_code
        return Response(self.response_format)


class CategoryIndex(APIView):
    def get(self, request):
        try:
            search = request.query_params["search"]
            queryset = Brand.objects.filter(brands__brand_name__contains=search)
            serializer = CategorySerializer(
                queryset, many=True, context={"request": request}
            )
            return Response({"data": serializer.data})
        except MultiValueDictKeyError:
            queryset = Brand.objects.all()
            serializer = CategorySerializer(queryset, many=True)
            return Response(serializer.data)


class PopularView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(PopularView, self).__init__(**kwargs)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    )
    search_fields = (
        "product_name",
        "product_category",
    )
    filter_class = ProductFilter
    ordering_fields = ("views",)
    http_method_names = ("get",)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response_data = super(PopularView, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)
