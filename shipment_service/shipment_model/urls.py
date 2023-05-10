from django.urls import path
from . import views

urlpatterns = [
    path("shipment_status/<int:oid>/", views.GetShipmentAPIView.as_view(), name = "shipment_status"),
    path("shipment_regis/", views.RegisShipmentAPIView.as_view(), name = "shipment_regis"),
]