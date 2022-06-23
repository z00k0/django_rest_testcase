from rest_framework import serializers
from rest_framework.fields import IntegerField

from .models import Client, Bill


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    organizations = IntegerField()
    total_amount = IntegerField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'organizations', 'total_amount']