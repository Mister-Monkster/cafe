from rest_framework import serializers
from .models import Orders, OrderItem, Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'price']


class OrdersItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrdersSerializer(serializers.ModelSerializer):
    items = OrdersItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'table_number', 'status', 'created_at', 'updated_at', 'items']