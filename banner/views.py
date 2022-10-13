from rest_framework.views import APIView
from .models import Banner
from .serializers import BannerSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class BannerIndex(APIView):
    def get(self, request):
        queryset = Banner.objects.all()
        serializer = BannerSerializer(queryset, many=True, context={"request": request})
        return Response({"data": serializer.data})
