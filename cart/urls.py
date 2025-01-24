from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("detail/", views.CartView.as_view(), name="cart"),
    path("add/", views.CartAddView.as_view(), name="cart-add"),
    path("remove/", views.CartRemoveView.as_view(), name="cart-remove"),
    path("clear/", views.CartClearView.as_view(), name="cart-clear"),
]