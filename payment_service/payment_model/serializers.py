from django.urls import reverse
from rest_framework import serializers

from .models import payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = payment
        fields = '__all__'