from django.urls import reverse
from rest_framework import serializers

from .models import user, customer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = customer
        fields = '__all__'
