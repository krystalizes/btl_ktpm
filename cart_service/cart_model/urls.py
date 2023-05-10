from django.urls import path
from . import views

urlpatterns = [
    path("get_cart/<int:uid>/", views.get_cart_data, name = "get_cart"),
    path("cart_regis/", views.cart_regis, name = "cart_regis"),
    path("cart_update/<int:uid>/<str:pid>/", views.update_cart, name = "cart_update"),
    path("cart_delete_product/<int:uid>/<str:pid>/", views.cart_delete_product, name = "cart_delete"),
    path("cart_delete_all/<int:uid>/", views.cart_delete, name = "cart_delete"),
]