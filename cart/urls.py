from django.urls import path

from .views import CartView, CartAddView, CartRemoveView

app_name = "cart"

urlpatterns = [
    path('detail/', CartView.as_view(), name='cart'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('remove/', CartRemoveView.as_view(), name='cart-remove'),
]