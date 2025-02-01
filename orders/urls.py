from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.OrderCreateView.as_view(), name="order-create"),
    path("<int:order_id>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("<int:order_id>/pay/", views.OrderPayView.as_view(), name="order-pay"),
    path("verify/",views.OrderVerifyView.as_view(), name="order-verify"),
    path("apply/", views.CouponApplyView.as_view(), name="apply-coupon"),
]