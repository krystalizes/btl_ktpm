from django.urls import path
from . import views

urlpatterns = [
    path("getallshoe/", views.GetAllShoesAPIView.as_view(), name = "getallshoe"),
    path("shoe_regis/", views.RegisShoeAPIView.as_view(), name = "shoe_regis"),
    path("shoe_info/<str:id>/", views.GetshoeinfoAPIView.as_view(), name = "shoe_info"),
    path("shoe_update/<str:id>/", views.UpdateShoeAPIView.as_view(), name = "shoe_update"),
    path("shoe_delete/<str:id>/", views.DeleteShoeAPIView.as_view(), name = "shoe_delete"),
]