from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .cart import Cart
from .serializers import CartItemSerializer, CartAddSerializer

class CartView(APIView):
    """ API view to retrieve the contents of the user's cart.
    Requires authentication. """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        cart_data = list(cart)  # Get the cart data as a list of dictionaries
        ser_data = CartItemSerializer(cart_data, many=True)
        return Response(ser_data.data)

class CartAddView(APIView):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Remove a product from the cart. """
        
        product_id = request.data["product_id"]
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request)
        try:
            cart.remove(product_id)
            return Response({"message": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)