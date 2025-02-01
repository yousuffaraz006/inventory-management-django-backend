from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *

def company_member_profile(sender, instance, created, **kwargs):
  if created:
    CompanyMember.objects.create(
      user=instance,
      name=instance.first_name + instance.last_name,
    )
    print('Company Member Created!')
post_save.connect(company_member_profile, sender=User)