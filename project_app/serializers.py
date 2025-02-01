from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'username', 'password']

class CompanySerializer(ModelSerializer):
  class Meta:
    model = Companie
    fields = ['id', 'company_name', 'company_phone', 'company_email', 'company_address']

class CompanyMemberSerializer(ModelSerializer):
  class Meta:
    model = CompanyMember
    fields = ['id', 'company', 'member_name', 'admin', 'member_email', 'member_phone', 'member_verified']

class ProductSerializer(ModelSerializer):
  class Meta:
    model = Product
    fields = ['id', 'company', 'product_created_by', 'product_created_date', 'product_name', 'product_rate']

class PurchaseItemSerializer(ModelSerializer):
  p_item_product = ProductSerializer()

  class Meta:
    model = PurchaseItem
    fields = ['id', 'purchase', 'p_item_product', 'p_item_quantity', 'p_item_cost']

class PurchaseSerializer(ModelSerializer):
  items = PurchaseItemSerializer(many=True)
  company = CompanySerializer()

  class Meta:
    model = Purchase
    fields = ['id', 'company', 'purchase_created_by', 'purchase_slug', 'purchase_date', 'purchase_total', 'items']

class CustomerSerializer(ModelSerializer):
  class Meta:
    model = Customer
    fields = ['id', 'company', 'customer_name', 'customer_email', 'customer_phone']

class SaleItemSerializer(ModelSerializer):
  s_item_product = ProductSerializer()

  class Meta:
    model = SaleItem
    fields = ['id', 'sale', 's_item_product', 's_item_quantity', 's_item_price']

class SaleSerializer(ModelSerializer):
  items = SaleItemSerializer(many=True)
  sale_customer = CustomerSerializer()
  company = CompanySerializer()

  class Meta:
    model = Sale
    fields = ['id', 'company', 'sale_created_by', 'sale_slug', 'sale_date', 'sale_customer', 'sale_total', 'items']