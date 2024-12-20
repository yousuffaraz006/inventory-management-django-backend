from django.contrib import admin
from .models import *

class CompanyDisplay(admin.ModelAdmin):
  list_display = ('founder', 'company_name', 'company_phone', 'company_email', 'company_address')

class CompanyMemberDisplay(admin.ModelAdmin):
  list_display = ('company', 'member_name', 'admin', 'member_email', 'member_phone', 'member_verified')

class ProductDisplay(admin.ModelAdmin):
  list_display = ('company', 'product_created_by', 'product_created_date', 'product_name', 'product_rate')

class PurchaseDisplay(admin.ModelAdmin):
  list_display = ('company', 'purchase_created_by', 'purchase_slug', 'purchase_date', 'purchase_total')

class PurchaseItemDisplay(admin.ModelAdmin):
  list_display = ('purchase', 'p_item_product', 'p_item_quantity', 'p_item_cost')

class CustomerDisplay(admin.ModelAdmin):
  list_display = ('company', 'customer_name', 'customer_email', 'customer_phone')

class SaleDisplay(admin.ModelAdmin):
  list_display = ('company', 'sale_created_by', 'sale_slug', 'sale_date', 'sale_customer', 'sale_total')

class SaleItemDisplay(admin.ModelAdmin):
  list_display = ('sale', 's_item_product', 's_item_quantity', 's_item_price')

admin.site.register(Companie, CompanyDisplay)
admin.site.register(CompanyMember, CompanyMemberDisplay)
admin.site.register(Product, ProductDisplay)
admin.site.register(Purchase, PurchaseDisplay)
admin.site.register(PurchaseItem, PurchaseItemDisplay)
admin.site.register(Customer, CustomerDisplay)
admin.site.register(Sale, SaleDisplay)
admin.site.register(SaleItem, SaleItemDisplay)