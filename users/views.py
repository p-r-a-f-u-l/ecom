import stripe
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializes import ProductSerializer

from .models import Address, CardDetails, FavDetails, CartDetails, Payment, MasterCart
from .serializers import AddCartSerializer, CardInfoSerializer, AddressInfoSerializer, FavItemSerializer, \
    AddFavItemSerializer, \
    CartSerializer, PaymentInfoSerializer, MasterCartSerializer

stripe.api_key = 'sk_test_51KlPR4SIjngpG4VN08PLkiMp1C17JEE4oRjHRERK8EcUb7wz6SFjEu653FDkHVbAEYyFbfABZPILV90PsBdvCJ6o00X5SIHg9q'


class AddressIndex(ModelViewSet):
    serializer_class = AddressInfoSerializer
    http_method_names = ("get", "post", "delete", "put")

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        super(AddressIndex, self).list(request, *args, **kwargs)
        address = Address.objects.filter(user_id=request.user.id)
        serializer = AddressInfoSerializer(address, many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CardIndex(ModelViewSet):
    serializer_class = CardInfoSerializer
    http_method_names = ("get", "post", "delete", "put")

    def get_queryset(self):
        return CardDetails.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        super(CardIndex, self).list(request, *args, **kwargs)
        card = CardDetails.objects.filter(owner_id=request.user.id)
        serializer = CardInfoSerializer(card, many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


class FavItemIndex(APIView):
    def get(self, request):
        query = Product.objects.filter(favourite=request.user)
        # filterquery = query.favourite.filter(id=request.user.id)
        serializers = ProductSerializer(query, many=True, context={'request': request})
        return Response({"data": serializers.data})


class AddFaveItemIndex(ModelViewSet):
    serializer_class = AddFavItemSerializer
    http_method_names = ('post',)

    def get_queryset(self):
        return FavDetails.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MasterCartIndex(ModelViewSet):
    queryset = MasterCart.objects.all()
    serializer_class = MasterCartSerializer


class CartIndex(ModelViewSet):
    serializer_class = CartSerializer
    http_method_names = ("get", "patch", "delete")

    def get_queryset(self):
        return CartDetails.objects.filter(owner_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        super(CartIndex, self).list(request, *args, **kwargs)
        card = CartDetails.objects.filter(owner_id=request.user.id)
        serializer = CartSerializer(card, many=True, context={"request": request})
        # c = sum([item.quantity for item in card])
        # t = sum([serializer.price])
        info = {"status": status.HTTP_200_OK, "data": serializer.data}
        return Response(info)


class AddCartItemIndex(ModelViewSet):
    serializer_class = AddCartSerializer
    http_method_names = ('post',)

    def get_queryset(self):
        return CartDetails.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PaymentIndex(ModelViewSet):
    serializer_class = PaymentInfoSerializer
    http_method_names = ('post',)

    def get_queryset(self):
        return Payment.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PaymentIndexSe(APIView):
    def get(self, request):
        payment = Payment.objects.filter(owner_id=self.request.user.id).all()
        serializer = PaymentInfoSerializer(payment, many=True)
        demo = stripe.Charge.retrieve('ch_3KoKnSSIjngpG4VN0tSjJYcs', )
        print(demo)
        return Response({'data': serializer.data})


class PaymentIndexID(APIView):
    def get(self, request, pk):
        payment = get_object_or_404(
            Payment, pk=pk, owner_id=self.request.user.id)
        serializer = PaymentInfoSerializer(payment)
        print(serializer.data.pop('payment_code'))
        code = serializer.data.pop('payment_code')
        demo = stripe.Charge.retrieve(code, )
        # print(demo.py)
        return Response({'data': demo})
