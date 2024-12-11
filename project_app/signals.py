from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *

def customer_profile(sender, instance, created, **kwargs):
  if created:
    group = Group.objects.get(name='employer')
    instance.groups.add(group)
    Company.objects.create(
      user=instance,
      name=instance.first_name,
    )
    print('Company Created!')

post_save.connect(customer_profile, sender=User)