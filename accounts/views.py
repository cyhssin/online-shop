from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .serializers import (UserSerializer,
    LoginSerializer,
    LogoutSerializer,
    OTPVerificationSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer,
    )
from .authentication import authenticate

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = UserSerializer(data=request.data)

        if ser_data.is_valid():
            ser_data.save()
            return Response({"message": "Please check your email for the OTP."}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = OTPVerificationSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(
                {"message": "Your account has been activated"}, 
                status=status.HTTP_200_OK
            )
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = LoginSerializer(data=request.data)
        if ser_data.is_valid():
            username = ser_data.data.get("username")
            password = ser_data.data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                })
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = LogoutSerializer(data=request.data)
        if ser_data.is_valid():
            refresh_token = ser_data.validated_data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "you logged out successfully!!"}, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordRestView(APIView):
    """ Handles password reset requests by sending an OTP to the user's email. """

    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = PasswordResetSerializer(data=request.data)

        if ser_data.is_valid():
            ser_data.save()
            return Response(
                {"message": "OTP has been sent to your email"}, 
                status=status.HTTP_200_OK
            )
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    """ This view is accessible to any user and processes the password change. """

    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = ChangePasswordSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(
                {"message": "Password has been reset successfully"}, 
                status=status.HTTP_200_OK
            )
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)