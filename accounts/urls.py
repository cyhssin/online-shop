from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("verify_otp/", views.OTPVerificationView.as_view(), name="verify-otp"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("password_reset/", views.UserPasswordRestView.as_view(), name="password-reset-attempt"),
    path("password_reset_confirm/", views.ResetPasswordView.as_view(), name="password-reset"),
]