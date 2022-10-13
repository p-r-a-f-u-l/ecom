from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OfferModel
from .serializers import OfferModelSerializer
from rest_framework import status


class OfferView(APIView):
    def get(self, request):
        query = OfferModel.objects.all()
        serializer = OfferModelSerializer(query, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
