from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.ProductList.as_view(), name="product_list"),
    path("<slug:category>/", views.ProductList.as_view(), name="product_list_by_category"),
    path("products/<slug:slug>/", views.ProductDetail.as_view(), name="product_detail"),
    path("bucket/", views.BucketProduct.as_view(), name="bucket"),
    path("delete_obj/<str:ey>/", views.DeleteBucketObject.as_view(), name="delete_obj_bucket"),
	path("download_obj/<str:key>/", views.DownloadBucketObject.as_view(), name="download_obj_bucket"),
]