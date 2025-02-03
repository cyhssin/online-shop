from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

from .models import User, OtpCode

class UserSerializer(serializers.ModelSerializer):
    """ Handles serialization and deserialization of User objects """

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True) 

    class Meta:
        model = User
        fields = ["email", "sur_name", "for_name", "password", "password2"] 
        extra_kwargs = {"password": {"write_only": True}} 

    def validate(self, attrs):
        """ Check if password and password2 match """

        password = attrs["password"]
        password2 = attrs["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs
        
    def save(self):        
        """ Create a new user """

        email = self.validated_data["email"]
        # Generate OTP using model method
        otp_instance = OtpCode.generate_otp(email)
        
        # Send email
        send_mail(
            "Verify Email",
            f"Your OTP code for active account is: {otp_instance.code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        user = User(
            email=self.validated_data["email"],
            sur_name=self.validated_data["sur_name"],
            for_name=self.validated_data["for_name"]
        )
        user.set_password(self.validated_data["password"]) 
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """ Handles user login with username and password """

    username = serializers.CharField()
    password = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    """ Handles user logout with refresh token """
    refresh_token = serializers.CharField()

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            otp_obj = OtpCode.objects.get(email=data["email"])
            if otp_obj.code != data["otp_code"]:
                raise serializers.ValidationError("Invalid OTP")
        except OtpCode.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")
        return data
    
    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        # Delete used OTP
        OtpCode.objects.filter(email=email).delete()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self):
        email = self.validated_data["email"]
        # Generate OTP using model method
        otp_instance = OtpCode.generate_otp(email)
        
        # Send email
        send_mail(
            "Password Reset OTP",
            f"Your OTP code for password reset is: {otp_instance.code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords don't match")

        try:
            otp_obj = OtpCode.objects.get(email=data["email"])
            if otp_obj.code != data["otp_code"]:
                raise serializers.ValidationError("Invalid OTP")
        except OtpCode.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")

        return data

    def save(self):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Delete used OTP
        OtpCode.objects.filter(email=email).delete()