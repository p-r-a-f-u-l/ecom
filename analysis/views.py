from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import AnalysisProduct, RecentProduct
from .serializers import AnalysisProductSerializer, RecentlyProductSerializer


class Analysis(APIView):
    def get(self, request):
        print(self.request)
        queryset = AnalysisProduct.objects.all()
        serializer = AnalysisProductSerializer(queryset, many=True)
        return Response({"msg": serializer.data})


class RecentlyView(APIView):
    def get(self, request):
        query = RecentProduct.objects.filter(owner=request.user.id).order_by(
            "-create_at"
        )[:5]
        serializer = RecentlyProductSerializer(query, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
