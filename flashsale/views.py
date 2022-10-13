from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from flashsale.serializers import FlashSaleSerializer, FlashSerializer

from .models import FlashSale, FlashSaleProduct


class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "data": args.get("data", [])
        }


class FlashIndex(APIView):
    def get(self, request):
        queryset = FlashSale.objects.all()
        serializer = FlashSerializer(
            queryset, many=True, context={'request': request})
        try:
            time = serializer.data[0]['created_at'][:26].replace("T", " ")
            server_time = datetime.strptime(
                time, '%Y-%m-%d %H:%M:%S.%f')
            end_time = server_time + timedelta(hours=24)
            current_time = timezone.now().strftime('%Y-%d-%m %H:%M:%S.%f')
            current_time = datetime.strptime(
                current_time, '%Y-%d-%m %H:%M:%S.%f')

            print(f"{current_time}\n{end_time}")

            if current_time >= end_time:
                queryset.delete()

            return Response({"data": serializer.data})

        except IndexError:
            print("error")
            return Response({"status": "FLASHSALE IS END"})


class FlashIdIndex(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(FlashIdIndex, self).__init__(**kwargs)

    queryset = FlashSaleProduct.objects.all()
    serializer_class = FlashSaleSerializer
    http_method_names = ('get',)

    def list(self, request, *args, **kwargs):
        response_data = super(FlashIdIndex, self).list(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        return Response(self.response_format)
