from rest_framework import serializers

from .models import User

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