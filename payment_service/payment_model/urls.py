from django.urls import path
from . import views

urlpatterns = [
    path("payment_status/<int:oid>/", views.GetPaymentAPIView.as_view(), name = "payment_status"),
    path("payment_regis/", views.RegisPaymentAPIView.as_view(), name = "payment_regis"),
]