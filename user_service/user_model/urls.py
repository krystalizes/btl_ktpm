from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name = "login"),
    path("regis/", views.RegisAPIView.as_view(), name = "regis"),
    path("getuserinfo/<int:id>/", views.GetuserinfoAPIView.as_view(), name = "getuserinfo"),
    path("getcustomerinfo/<int:uid>/", views.GetCustomerExistAPIView.as_view(), name = "getcustomerinfo"),
    path("updateuser/<int:id>/", views.UpdateUserAPIView.as_view(), name = "updateuser"),
    path("regiscustomer/", views.RegisCustomerAPIView.as_view(), name = "regiscustomer"),
    path("deleteuser/<int:id>/", views.DeleteUserAPIView.as_view(), name = "deleteuser"),
    path("updatecustomer/<int:uid>/", views.UpdateCustomerAPIView.as_view(), name = "updatecustomer"),
    path("getcustomerinfo2/<int:uid>/", views.GetCustomerinfoAPIView.as_view(), name = "getcustomerinfo2"),
]