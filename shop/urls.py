from django.urls import path, include

from . import views

app_name = "shop"

bucket_urls = [
    path("", views.BucketProductView.as_view(), name="bucket"),
    path("delete_obj/<str:key>/", views.DeleteBucketObjectView.as_view(), name="delete_obj_bucket"),
    path("download_obj/<str:key>/", views.DownloadBucketObjectView.as_view(), name="download_obj_bucket"),
]

urlpatterns = [
    path("bucket/", include(bucket_urls)),
    path("", views.ProductListView.as_view(), name="product_list"),
    path("<slug:category>/", views.ProductListView.as_view(), name="product_list_by_category"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]