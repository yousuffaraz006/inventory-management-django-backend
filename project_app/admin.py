from django.contrib import admin
from .models import *

class ProductDisplay(admin.ModelAdmin):
  list_display = ('company', 'name', 'rate')

class CompanyDisplay(admin.ModelAdmin):
  list_display = ('name', 'email', 'address')

class PurchaseDisplay(admin.ModelAdmin):
  list_display = ('slug', 'company', 'date', 'total')

class PurchaseItemDisplay(admin.ModelAdmin):
  list_display = ('purchase', 'product', 'quantity', 'cost')

class EmployeeDisplay(admin.ModelAdmin):
  list_display = ('company', 'name', 'email', 'phone', 'verified')

admin.site.register(Company, CompanyDisplay)
admin.site.register(Product, ProductDisplay)
admin.site.register(Purchase, PurchaseDisplay)
admin.site.register(PurchaseItem, PurchaseItemDisplay)
admin.site.register(Employee, EmployeeDisplay)