# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """ Serializer for OrderItem model. """
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model. Includes nested serialization for order items. """

    items = OrderItemSerializer(many=True, read_only=True)  # Nested serializer for order items

    class Meta:
        model = Order
        fields = ["id", "user", "paid", "created", "updated", "discount", "items"]