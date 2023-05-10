from django.urls import path
from . import views

urlpatterns = [
    path("getproduct/", views.get_product_data, name = "getproduct"),
]