# urls.py
from django.urls import path

from .views import OrderDetailView, OrderCreateView

app_name = "orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
]