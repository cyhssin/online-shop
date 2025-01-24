from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .cart import Cart
from .serializers import (CartItemSerializer, CartAddSerializer,
    CartRemoveSerializer,)

class CartView(APIView):
    """ API view to retrieve the contents of the user's cart.
    Requires authentication. """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        cart_data = list(cart)  # Get the cart data as a list of dictionaries
        ser_data = CartItemSerializer(cart_data, many=True)
        return Response({
            "cart": ser_data.data,
            "total_price": str(total_price)
        })

class CartAddView(APIView):
    """ API view to add a product to the cart. """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Add a product to the cart. """
        
        ser_data = CartAddSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        cart = Cart(request)
        product_id = ser_data.validated_data["product_id"]
        quantity = ser_data.validated_data["quantity"]

        try:
            cart.add(product_id, quantity)
            return Response({"message": "Product added to cart"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartRemoveView(APIView):
    """ API view to remove a product from the cart. """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Remove a product from the cart using the provided product_id. """

        serializer = CartRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]

        cart = Cart(request)
        try:
            cart.remove(product_id)
            return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)  # Use HTTP 200
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartClearView(APIView):
    """ API view to clear the entire cart. """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Clear all items from the cart.
        """
        cart = Cart(request)
        cart.clear()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)