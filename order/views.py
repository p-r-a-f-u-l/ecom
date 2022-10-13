import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import CartDetails
from .models import Order, OrderID, OrderStatus, Order_Status
from .serializers import OrderIdSerializer, OrderStatusSerializer


class OrderIndex(APIView):
    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderStatusSerializer(queryset, many=True)
        return Response({"data": serializer.data})


class OrderIDIndex(ModelViewSet):
    queryset = Order
    serializer_class = OrderStatusSerializer
    http_method_names = ("get",)

    # def get(self, request, pk):
    #     queryset = Order.objects.filter(pk=pk).filter(user=request.user)
    #     serializer = OrderStatusSerializer(queryset, many=True)
    #     return Response({"data": serializer.data})

    # def patch(self, request, pk):
    #     queryset = Order.objects.filter(pk=pk)
    #     if request.data["order_status"] == "canceled":
    #         try:
    #             queryset.update(order_status=request.data["order_status"])
    #         except KeyError:
    #             return Response({"msg": "Error.. param must pass..!!"})
    #     return Response({'data': f'Ordered {request.data["order_status"]}..!!'})


class CheckPinCode(APIView):
    def post(self, request):
        pincode = request.data.get("pin")
        if pincode is None:
            data = {
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "data": "Only Accept Pincode with valid Param",
            }
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        else:
            pincode = request.data.get("pin")
            print(pincode)
            today = datetime.date.today() + datetime.timedelta(days=4)
            data = {
                "status": status.HTTP_200_OK,
                "data": f"Delivery by {today.strftime('%d %b')} | Free",
            }
            return Response(data=data, status=status.HTTP_200_OK)


class OrderInfoInex(APIView):
    def post(self, request):
        try:
            status = request.data.get("status")
            payid = request.data.get("order_id")
            orderid = request.data.get("address_id")
            phone = request.data.get("phone_no")
            quantities = request.data.get("quantity")
            amount = request.data.get("amount")
            datas = {
                "stripe_id": payid,
                "address_id": orderid,
                "phone_no": phone,
                "status": status,
                "quantity": quantities,
                "amount": amount,
            }
        except ValueError:
            return Response({"status": "Id tho sahi dal bhai.."})

        if not OrderID.objects.filter(stripe_id=payid).exists():
            if status == "succeeded":
                # productquery = get_object_or_404(CartDetails, pk=cart_id)
                serializer = OrderIdSerializer(data=datas)
                serializer.is_valid(raise_exception=True)
                serializer.save(owner=request.user)

                checkdb = get_object_or_404(
                    OrderID, stripe_id=serializer.data.get("stripe_id")
                )

                queryset = Order.objects.all()

                # queryset.create(user=request.user, order_info=checkdb)

                queryset.create(
                    user=request.user,
                    order_info=checkdb,
                    quantity=quantities,
                    total_amount=amount,
                )
                card = CartDetails.objects.filter(owner_id=request.user.id).all()
                # serializer = CartSerializer(card, many=True, context={"request": request})
                card.delete()
                return Response({"status": status})

        return Response({"status": "Already Exists"})
