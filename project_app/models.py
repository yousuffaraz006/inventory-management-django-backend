from django.contrib.auth.models import User
from django.db import models
import random

class Company(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=255, unique=True, null=True, blank=True)
  email = models.CharField(max_length=25, unique=True, null=True, blank=True)
  address = models.CharField(max_length=255, null=True, blank=True)

  def __str__(self):
    return self.name

class Employee(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255, null=True, blank=True)
  email = models.CharField(max_length=25, unique=True, null=True, blank=True)
  phone = models.IntegerField(null=True, blank=True)
  verified = models.BooleanField(default=False)

  def __str__(self):
    return self.name

class Product(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=75, null=True, blank=True)
  rate = models.FloatField(null=True, blank=True)

  def __str__(self):
    return self.name

class Purchase(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
  slug = models.SlugField(unique=True, null=True, blank=True)
  date = models.DateTimeField(auto_now_add=True)
  total = models.FloatField(null=True, blank=True)

  def __str__(self):
    return self.slug

  def save(self, *args, **kwargs):
    if not self.slug:
      slug_identifier = self.company.name[:3].upper()
      slug_base = random.randint(100, 999)
      slug_id = random.randint(10000000, 99999999)
      self.slug = f"#{slug_identifier}{slug_base}-{slug_id}"
    super(Purchase, self).save(*args, **kwargs)

class PurchaseItem(models.Model):
  purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
  cost = models.FloatField(null=True, blank=True)
  quantity = models.IntegerField(null=True, blank=True)