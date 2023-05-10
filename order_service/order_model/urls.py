from django.urls import path
from . import views

urlpatterns = [
    path("regisorder/", views.RegisOrderAPIView.as_view(), name = "regisorder"),
    path("getorderinfo/<int:id>/", views.GetOrderAPIView.as_view(), name = "getorderinfo"),
    path("getcustomerorderlist/<int:uid>/", views.GetOrderlistCustomerAPIView.as_view(), name = "getcustomerorderlist"),
]