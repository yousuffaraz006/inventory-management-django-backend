from django.urls import path
from .views import *

urlpatterns = [
  path('', Homepage, name='homepage'),
  path('company/', Company, name='company'),
  path('employee/<str:pk>/', EmployeeDetail, name='employeeDetail'),
  path('search-products/', search_products, name='search-products'),
  path('products/', Products, name='products'),
  path('product/<str:pk>/', ProductDetail, name='product'),
  path('search-purchases/', search_purchases, name='search-purchases'),
  path('all-purchases/', AllPurchases, name='all-purchases'),
  path('purchases/', Purchases, name='purchases'),
  path('customers/', Customers, name='customers'),
  path('search-sales/', search_sales, name='search-sales'),
  path('all-sales/', AllSales, name='all-sales'),
  path('sales/', Sales, name='sales'),
]