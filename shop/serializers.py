from rest_framework import serializers

from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["category", "name", "slug", "image", "description",
                    "price", "available", "created", "updated"]

class BucketObjectSerializer(serializers.Serializer):
    ...

class DownloadBucketObject(serializers.Serializer):
    ...

class DeleteBucketObject(serializers.Serializer):
    ...