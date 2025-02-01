import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings as s
from django.utils import timezone

from .models import Order, OrderItem, Coupon
from .serializers import OrderSerializer, CouponApplySerializer
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

class CouponApplyView(APIView):
    """ API view to apply a coupon to an order. """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = CouponApplySerializer(data=request.data)
        if not ser_data.is_valid():
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        coupon_code = ser_data.validated_data["coupon"]
        order_id = ser_data.validated_data["order_id"]

        now_time = timezone.now()
        try:
            coupon = Coupon.objects.get(
                code__exact=coupon_code,
                valid_from__lte=now_time,
                valid_to__gte=now_time,
                active=True
            )
        except Coupon.DoesNotExist:
            return Response(
                {"error": "Invalid or expired coupon code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(Order, id=order_id, user=request.user)

        order.discount = coupon.discount
        order.save()

        return Response(
            {"message": "Coupon applied successfully.", "discount": coupon.discount},
            status=status.HTTP_200_OK
        )
        
class OrderPayView(APIView):
    """ API view to handle payment for an order using Zarinpal."""

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """
        Initiate payment for an order using Zarinpal.
        """

        order = get_object_or_404(Order, id=order_id)

        CALLBACK_URL = f"{s.CALLBACK_URL}?order_id={order.id}"  

        data = {
            "merchant_id": s.MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CALLBACK_URL,
            "description": s.DESCRIPTION,
        }
        data = json.dumps(data)

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "content-length": str(len(data))
        }

        try:
            # Send payment request to Zarinpal
            response = requests.post(s.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response_data = response.json()

                # Check if the payment request was successful
                if response_data.get("data", {}).get("authority"):
                    # Return payment URL and authority code
                    return Response({
                        "status": True,
                        "url": s.ZP_API_STARTPAY + str(response_data["data"]["authority"]),
                        "authority": response_data["data"]["authority"]
                    }, status=status.HTTP_200_OK)
                else:
                    # Handle Zarinpal errors
                    errors = response_data.get("errors", {})
                    return Response({
                        "status": False,
                        "code": errors.get("code", "Unknown error"),
                        "message": errors.get("message", "No error message provided")
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle non-200 responses
            return Response({
                "status": False,
                "code": "Zarinpal API error",
                "details": response.text
            }, status=response.status_code)

        except requests.exceptions.Timeout:
            # Handle timeout errors
            return Response({
                "status": False,
                "code": "timeout"
            }, status=status.HTTP_408_REQUEST_TIMEOUT)

        except requests.exceptions.ConnectionError:
            # Handle connection errors
            return Response({
                "status": False,
                "code": "connection error"
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class OrderVerifyView(APIView):
    """ Verify payment for an order using Zarinpal's callback. """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.query_params.get("order_id")
        if not order_id:
            return Response({"status": False, "message": "Order ID not found in query params"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=int(order_id))
        t_status = request.query_params.get("Status")
        t_authority = request.query_params.get("Authority")

        if t_status != "OK":
            return Response({"status": False, "message": "Transaction failed or canceled by user"}, status=status.HTTP_400_BAD_REQUEST)

        req_data = {
            "merchant_id": s.MERCHANT,
            "amount": order.get_total_price(),
            "authority": t_authority,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        try:
            # Send verification request to Zarinpal
            response = requests.post(s.ZP_API_VERIFY, data=json.dumps(req_data), headers=headers, timeout=10)
            response.raise_for_status()
            response_data = response.json()

            if not isinstance(response_data, dict):
                return Response({
                    "status": False,
                    "message": "Invalid Zarinpal API response",
                    "details": "Expected a dictionary, got a list or other type"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check for Zarinpal API errors
            if "errors" in response_data and response_data["errors"]:
                return Response({
                    "status": False,
                    "message": "Zarinpal API error",
                    "error_code": response_data["errors"].get("code", "Unknown error"),
                    "error_message": response_data["errors"].get("message", "No error message provided")
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check payment status
            if "data" not in response_data:
                return Response({
                    "status": False,
                    "message": "Invalid Zarinpal API response",
                    "details": "Missing 'data' field in response"
                }, status=status.HTTP_400_BAD_REQUEST)

            t_status = response_data["data"].get("code")
            if t_status == 100:
                # Payment was successful
                order.paid = True
                order.authority = t_authority
                order.save()
                return Response({
                    "status": True,
                    "message": "Transaction success",
                    "ref_id": response_data["data"].get("ref_id")
                }, status=status.HTTP_200_OK)
            else:
                # Payment failed
                return Response({
                    "status": False,
                    "message": "Transaction failed",
                    "details": response_data["data"].get("message", "No details provided")
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            # Handle request errors (e.g., timeout, connection error)
            return Response({
                "status": False,
                "message": "Zarinpal API request failed",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)