from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'username', 'password']
    
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user

class CompanySerializer(ModelSerializer):
  class Meta:
    model = Company
    fields = ['id', 'name', 'email', 'address']

class EmployeeSerializer(ModelSerializer):
  class Meta:
    model = Employee
    fields = ['id', 'company', 'name', 'email', 'phone', 'verified']

class ProductSerializer(ModelSerializer):
  class Meta:
    model = Product
    fields = ['id', 'company', 'name', 'rate']

class PurchaseItemSerializer(ModelSerializer):
  product = ProductSerializer()

  class Meta:
    model = PurchaseItem
    fields = ['id', 'purchase', 'product', 'quantity', 'cost']

class PurchaseSerializer(ModelSerializer):
  items = PurchaseItemSerializer(many=True)

  class Meta:
    model = Purchase
    fields = ['id', 'company', 'slug', 'date', 'total', 'items']