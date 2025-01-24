from rest_framework import serializers

from shop.models import Product
from shop.serializers import ProductSerializers

class CartItemSerializer(serializers.Serializer):
    """
    Serializer for cart items. Includes product details, quantity, price, and total price.
    """

    product = ProductSerializers()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        """
        Validate that the product ID corresponds to an existing product.
        """

        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

class CartRemoveSerializer(serializers.Serializer):
    """
    Serializer for removing a product from the cart.
    """
    
    product_id = serializers.IntegerField()