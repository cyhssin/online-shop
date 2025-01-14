from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializers, BucketObjectSerializer, DownloadBucketObject, DeleteBucketObject
from .tasks import all_bucket_objects_task, delete_object_task, download_object_task

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

class BucketProduct(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        objects = all_bucket_objects_task()
        ser_data = BucketObjectSerializer(objects, many=True)
        return Response({"ser_data": ser_data}, status=status.HTTP_200_OK)

class DownloadBucketObject(APIView):
	def get(self, request, key):
		download_object_task.download_object_task.delay(key)

class DeleteBucketObject(APIView):
	def get(self, request, key):
		delete_object_task.delete_object_task.delay(key)

