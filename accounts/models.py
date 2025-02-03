import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    sur_name = models.CharField(max_length=255)
    for_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["sur_name", "for_name"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

class OtpCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_otp(cls, email):
        otp_code = str(random.randint(100000, 999999))
        otp_instance, _ = cls.objects.update_or_create(
            email=email,
            defaults={"code": otp_code}
        )
        return otp_instance

    def __str__(self):
        return f"{self.email} - {self.code}"