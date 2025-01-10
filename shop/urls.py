from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.ProductList.as_view(), name="product-list"),
    path("products/<slug:slug>/", views.ProductDetail.as_view(), name="product-detail"),
]
