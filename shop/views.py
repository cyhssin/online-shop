from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializers

class ProductList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category=None):
        if category:
            products = Product.objects.filter(category__name=category)
        else:
            products = Product.objects.all()
        ser_data = ProductSerializers(products, many=True)
        return Response(ser_data.data)

class ProductDetail(APIView):
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug, available=True)
        except Product.DoesNotExist:
            raise ValueError("Not found product")

    def get(self, request, slug):
        product = self.get_object(slug)
        ser_data = ProductSerializers(product)
        return Response(ser_data.data, status=status.HTTP_200_OK)