# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    """ Serializer for OrderItem model. """
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity"]

class CouponSerializer(serializers.ModelSerializer):
    """ Serializer for the Coupon model. """
    
    class Meta:
        model = Coupon
        fields = ["code", "valid_from", "valid_to", "discount", "active"]

class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model. Includes nested serialization for order items. """

    items = OrderItemSerializer(many=True, read_only=True)  # Nested serializer for order items
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "paid", "created", "updated", "discount", "authority", "coupon", "items"]

class CouponApplySerializer(serializers.Serializer):
    """ Serializer for applying a coupon to an order.
    Validates the coupon code and ensures the order exists. """

    coupon = serializers.CharField(max_length=50)
    order_id = serializers.IntegerField()

    def validate_order_id(self, value):
        if not Order.objects.filter(id=value).exists():
            raise serializers.ValidationError("Order does not exist.")
        return value