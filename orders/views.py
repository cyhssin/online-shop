from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.cart import Cart

class OrderDetailView(APIView):
    """ API view to retrieve details of a specific order. """

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """
        Retrieve details of an order by its ID.
        """
        
        # Ensure the order belongs to the authenticated user
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCreateView(APIView):
    """ API view to create a new order from the items in the cart.
    Requires authentication."""

    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        """
        Create a new order and add items from the cart.
        """

        cart = Cart(request)
        if not cart:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order for the authenticated user
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"]
            )

        # Clear the cart after creating the order
        cart.clear()  

        # Serialize the created order and return it in the response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)