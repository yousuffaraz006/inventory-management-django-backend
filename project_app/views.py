from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, status
from .serializers import *
from .models import *

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['company_name'] = user.first_name
    token['username'] = user.username
    return token

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer

class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_products(request):
  query = request.query_params.get("search")
  products = Product.objects.filter(company=request.user.company).filter(Q(name__icontains=query) | Q(rate__icontains=query))
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Products(request):
  if request.method == 'GET':
    products = Product.objects.filter(company=request.user.company)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data.copy()
    data['company'] = request.user.company.id
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def ProductDetail(request, pk):
  product = Product.objects.get(id=pk)
  if request.method == 'GET':
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    data = request.data.copy()
    data['company'] = request.user.company.id
    serializer = ProductSerializer(product, data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_purchases(request):
  query = request.query_params.get("search")
  purchase = Purchase.objects.filter(company=request.user.company).filter(Q(slug__icontains=query) | Q(date__icontains=query) | Q(total__icontains=query)).order_by('-date')
  serializer = PurchaseSerializer(purchase, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Purchases(request):
  if request.method == 'GET':
    purchases = Purchase.objects.filter(company=request.user.company).order_by('-date')
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data
    purchase = Purchase.objects.create(
      company=request.user.company,
      total = data.get('total'),
    )
    purchase.save()
    items = data.get('items', [])
    for item in items:
      PurchaseItem.objects.create(
        purchase=purchase,
        product=Product.objects.get(id=item.get('product')),
        
        cost=item.get('cost'),
        quantity=item.get('quantity'),
      )
    serializer = PurchaseSerializer(purchase)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def Sales(request):
  if request.method == 'GET':
    purchases = Purchase.objects.filter(company=request.user.company).order_by('-date')
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    data = request.data
    purchase = Purchase.objects.get(id=data.get('id'))
    purchase.total = data.get('total')
    purchase.save()
    serializer = PurchaseSerializer(purchase)
    return Response(serializer.data, status=status.HTTP_200_OK)