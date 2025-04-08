from rest_framework import serializers
from .models import Customer, PotentialCustomer, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class CustomerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'instagram', 'status', 'category', 'category_id', 'created_at', 'updated_at']

class PotentialCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotentialCustomer
        fields = ['id', 'name', 'email', 'phone', 'instagram', 'created_at'] 