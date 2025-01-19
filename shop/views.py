from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Product
from .serializers import (
    ProductSerializers,
    BucketObjectSerializer,
)
from .tasks import all_bucket_objects_task, delete_object_task, download_object_task

class ProductListView(APIView):
    """ Endpoint for listing products with optional category filtering """

    permission_classes = [AllowAny]

    def get(self, request, category=None):
        if category:
            products = Product.objects.filter(category__name=category)
        else:
            products = Product.objects.all()
        ser_data = ProductSerializers(products, many=True)
        return Response(ser_data.data)

class ProductDetailView(APIView):
    """ Endpoint for retrieving detailed information of a specific product """

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

class BucketProductView(APIView):
    """ Endpoint for listing all objects in the bucket (admin only) """

    permission_classes = [IsAdminUser]

    def get(self, request):
        objects = all_bucket_objects_task()
        ser_data = BucketObjectSerializer(objects, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

class DownloadBucketObjectView(APIView):
    """ Endpoint for initiating download of an object from the bucket (admin only) """

    permission_classes = [IsAdminUser]

    def get(self, request, key):
        download_object_task.delay(key)
        return Response(
            {"message": "Download task initiated"}, status=status.HTTP_200_OK
        )

class DeleteBucketObjectView(APIView):
    """ Endpoint for initiating deletion of an object from the bucket (admin only) """

    permission_classes = [IsAdminUser]

    def get(self, request, key):
        delete_object_task.delay(key)
        return Response({"message": "Delete task initiated"}, status=status.HTTP_200_OK)