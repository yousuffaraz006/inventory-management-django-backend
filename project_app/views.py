from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import status
from urllib.parse import urlencode
from .serializers import *
from .models import *

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['name'] = str(user.first_name + ' ' + user.last_name)
    token['groups'] = list(user.groups.values_list('name', flat=True))
    try:
      company_name = user.companymember.company.company_name
    except AttributeError:
      company_name = ""
    token['company_name'] = company_name
    return token

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def Signup(request):
  data = request.data
  first_name = data.get('first_name')
  last_name = data.get('last_name')
  username = data.get('username')
  password = data.get('password')
  if not username or not password:
    return Response(
      {"error": "Username and password are required."},
      status=status.HTTP_400_BAD_REQUEST,
    )
  if User.objects.filter(username=username).exists():
    return Response(
      {"error": "Username already exists."},
      status=status.HTTP_400_BAD_REQUEST,
    )

  try:
    user = User.objects.create_user(
      first_name=first_name,
      last_name=last_name,
      username=username,
      password=password,
    )
    group = Group.objects.get(name="employer")
    user.groups.add(group)
    my_company = Companie.objects.create(
      founder=user,
    )
    CompanyMember.objects.create(
      company=my_company,
      member=user,
      admin=True,
      member_name=first_name + ' ' + last_name,
      member_email=username,
      member_verified=True,
    )
    return Response(
      {"message": "User created successfully.", "username": user.username},
      status=status.HTTP_201_CREATED,
    )
  except Exception as e:
    return Response(
      {"error": "An error occurred while creating the user.", "details": str(e)},
      status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def Company(request):
  my_company = Companie.objects.get(founder=request.user.companymember.company.founder)
  if request.method == 'GET':
    serializer = CompanySerializer(my_company)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    serializer = CompanySerializer(my_company, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Homepage(request):
  my_company = Companie.objects.get(founder=request.user)
  if request.method == 'GET':
    employees = CompanyMember.objects.filter(company=my_company).exclude(admin=True)
    serializer = CompanyMemberSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data
    employee = User.objects.create_user(
      first_name=data.get('first_name'),
      last_name=data.get('last_name'),
      username=data.get('username'),
      password=data.get('password'),
    )
    employee.save()
    employee_group = Group.objects.get(name='employee')
    employee.groups.add(employee_group)
    CompanyMember.objects.create(
        member=employee,
        company=my_company,
        member_name=data.get('first_name') + ' ' + data.get('last_name'),
        member_email=data.get('username'),
    )
    serializer = UserSerializer(employee)
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def EmployeeDetail(request, pk):
  employee = CompanyMember.objects.get(id=pk)
  if request.method == 'GET':
    serializer = CompanyMemberSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    serializer = CompanyMemberSerializer(employee, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    user = employee.member
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_products(request):
  query = request.query_params.get("search")
  products = Product.objects.filter(company=request.user.companymember.company).filter(Q(product_name__icontains=query) | Q(product_rate__icontains=query))
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Products(request):
  if request.method == 'GET':
    products = Product.objects.filter(company=request.user.companymember.company).order_by('-product_created_date')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data.copy()
    data['company'] = request.user.companymember.company.id
    data['product_created_by'] = request.user.username
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
    data['company'] = request.user.companymember.company.id
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
  purchase = Purchase.objects.filter(company=request.user.companymember.company).filter(Q(purchase_slug__icontains=query) | Q(purchase_date__icontains=query) | Q(purchase_total__icontains=query)).order_by('-purchase_date')
  serializer = PurchaseSerializer(purchase, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllPurchases(request):
  purchases = Purchase.objects.filter(company=request.user.companymember.company).order_by('-purchase_date')
  serializer = PurchaseSerializer(purchases, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Purchases(request):
  if request.method == 'GET':
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 2))
    offset = (page - 1) * page_size

    purchase = Purchase.objects.filter(company=request.user.companymember.company).order_by('-purchase_date')
    total_count = purchase.count()
    paginated_purchases = purchase[offset:offset + page_size]
    
    serializer = PurchaseSerializer(paginated_purchases, many=True)
    return Response({
        "count": total_count,
        "next": f"/purchases/?page={page + 1}" if offset + page_size < total_count else None,
        "previous": f"/purchases/?page={page - 1}" if page > 1 else None,
        "results": serializer.data,
    }, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data
    purchase = Purchase.objects.create(
      company=request.user.companymember.company,
      purchase_created_by=request.user.username,
      purchase_total = data.get('purchase_total'),
    )
    purchase.save()
    items = data.get('items', [])
    for item in items:
      PurchaseItem.objects.create(
        purchase=purchase,
        p_item_product=Product.objects.get(id=item.get('p_item_product')),
        p_item_cost=item.get('p_item_cost'),
        p_item_quantity=item.get('p_item_quantity'),
      )
    serializer = PurchaseSerializer(purchase)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Customers(request):
  if request.method == 'GET':
    customers = Customer.objects.filter(company=request.user.companymember.company).order_by('customer_name')
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data.copy()
    data['company'] = request.user.companymember.company.id
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_sales(request):
  query = request.query_params.get("search")
  sale = Sale.objects.filter(company=request.user.companymember.company).filter(Q(sale_slug__icontains=query) | Q(sale_date__icontains=query) | Q(sale_total__icontains=query)).order_by('-sale_date')
  serializer = SaleSerializer(sale, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllSales(request):
  sales = Sale.objects.filter(company=request.user.companymember.company).order_by('-sale_date')
  serializer = SaleSerializer(sales, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Sales(request):
  if request.method == 'GET':
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 2))
    offset = (page - 1) * page_size

    sale = Sale.objects.filter(company=request.user.companymember.company).order_by('-sale_date')
    total_count = sale.count()
    paginated_sales = sale[offset:offset + page_size]
    
    serializer = SaleSerializer(paginated_sales, many=True)
    return Response({
        "count": total_count,
        "next": f"/sales/?page={page + 1}" if offset + page_size < total_count else None,
        "previous": f"/sales/?page={page - 1}" if page > 1 else None,
        "results": serializer.data,
    }, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    data = request.data
    customer_id = data.get("sale_customer")
    customer = get_object_or_404(Customer, id=customer_id)
    sale = Sale.objects.create(
      company=request.user.companymember.company,
      sale_created_by=request.user.username,
      sale_customer=customer,
      sale_total = data.get('sale_total'),
    )
    sale.save()
    items = data.get('items', [])
    for item in items:
      SaleItem.objects.create(
        sale=sale,
        s_item_product=Product.objects.get(id=item.get('s_item_product')),
        s_item_price=item.get('s_item_price'),
        s_item_quantity=item.get('s_item_quantity'),
      )
    serializer = SaleSerializer(sale)
    return Response(serializer.data, status=status.HTTP_201_CREATED)