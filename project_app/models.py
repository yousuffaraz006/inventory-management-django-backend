from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
import random

class Companie(models.Model):
  founder = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  company_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
  company_phone = models.BigIntegerField(null=True, blank=True)
  company_email = models.CharField(max_length=25, unique=True, null=True, blank=True)
  company_address = models.CharField(max_length=255, null=True, blank=True)

  def __str__(self):
    return str(self.founder.username)

class CompanyMember(models.Model):
  company = models.ForeignKey(Companie, on_delete=models.CASCADE, null=True)
  member = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  admin = models.BooleanField(default=False)
  member_image = models.ImageField(upload_to='images/', null=True, blank=True)
  member_name = models.CharField(max_length=255, null=True, blank=True)
  member_email = models.CharField(max_length=25, unique=True, null=True, blank=True)
  member_phone = models.BigIntegerField(null=True, blank=True)
  member_verified = models.BooleanField(default=False)

  def __str__(self):
    return self.member_name

class Product(models.Model):
  company = models.ForeignKey(Companie, on_delete=models.CASCADE, null=True)
  product_created_by = models.CharField(max_length=200, null=True, blank=True)
  product_created_date = models.DateTimeField(default=now)
  product_name = models.CharField(max_length=75, null=True, blank=True)
  product_rate = models.FloatField(null=True, blank=True)

  def __str__(self):
    return self.product_name

class Purchase(models.Model):
  company = models.ForeignKey(Companie, on_delete=models.CASCADE, null=True)
  purchase_created_by = models.CharField(max_length=200, null=True, blank=True)
  purchase_slug = models.SlugField(unique=True, null=True, blank=True)
  purchase_date = models.DateTimeField(auto_now_add=True)
  purchase_total = models.FloatField(null=True, blank=True)

  def __str__(self):
    return self.purchase_slug

  def save(self, *args, **kwargs):
    if not self.purchase_slug:
      slug_identifier = self.company.company_name[:3].upper()
      slug_base = random.randint(100, 999)
      slug_id = random.randint(10000000, 99999999)
      self.purchase_slug = f"#{slug_identifier}{slug_base}-P{slug_id}"
    super(Purchase, self).save(*args, **kwargs)

class PurchaseItem(models.Model):
  purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, related_name="items")
  p_item_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
  p_item_cost = models.FloatField(null=True, blank=True)
  p_item_quantity = models.IntegerField(null=True, blank=True)

class Customer(models.Model):
  company = models.ForeignKey(Companie, on_delete=models.CASCADE, null=True)
  customer_name = models.CharField(max_length=255, null=True, blank=True)
  customer_email = models.CharField(max_length=25, unique=True, null=True, blank=True)
  customer_phone = models.BigIntegerField(null=True, blank=True)

  def __str__(self):
    return self.customer_name

class Sale(models.Model):
  company = models.ForeignKey(Companie, on_delete=models.CASCADE, null=True)
  sale_created_by = models.CharField(max_length=200, null=True, blank=True)
  sale_slug = models.SlugField(unique=True, null=True, blank=True)
  sale_date = models.DateTimeField(auto_now_add=True)
  sale_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
  sale_total = models.FloatField(null=True, blank=True)

  def __str__(self):
    return self.sale_slug

  def save(self, *args, **kwargs):
    if not self.sale_slug:
      slug_identifier = self.company.company_name[:3].upper()
      slug_base = random.randint(100, 999)
      slug_id = random.randint(10000000, 99999999)
      self.sale_slug = f"#{slug_identifier}{slug_base}-S{slug_id}"
    super(Sale, self).save(*args, **kwargs)

class SaleItem(models.Model):
  sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, related_name="items")
  s_item_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
  s_item_price = models.FloatField(null=True, blank=True)
  s_item_quantity = models.IntegerField(null=True, blank=True)