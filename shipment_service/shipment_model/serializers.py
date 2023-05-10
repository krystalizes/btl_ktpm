from django.urls import reverse
from rest_framework import serializers

from .models import shipment


class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = shipment
        fields = '__all__'