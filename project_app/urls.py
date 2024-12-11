from django.urls import path
from .views import *

urlpatterns = [
  path('products/', Products, name='products'),
  path('product/<str:pk>/', ProductDetail, name='product'),
  path('search-products/', search_products, name='search-products'),
  path('purchases/', Purchases, name='purchases'),
  path('search-purchases/', search_purchases, name='search-purchases'),
]