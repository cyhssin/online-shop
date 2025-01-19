from rest_framework import serializers

from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    """ Serializer for the Product model """

    class Meta:
        model = Product
        fields = ["category", "name", "slug", "image", "description",
                  "price", "available", "created", "updated"]

class BucketObjectSerializer(serializers.Serializer):
    """ Serializer for individual objects in the bucket """

    key = serializers.CharField(source="Key")
    last_modified = serializers.DateTimeField(source="LastModified")
    size = serializers.IntegerField(source="Size")

class DownloadBucketObject(serializers.Serializer):
    """ Serializer for downloading a specific bucket object using its key """

    key = serializers.CharField(max_length=200)

class DeleteBucketObject(serializers.Serializer):
    """ Serializer for deleting a specific bucket object using its key """
    key = serializers.CharField(max_length=200)