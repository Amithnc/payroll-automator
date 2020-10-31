from .models import latestmonth,payroll
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=payroll)
def update_latestmonth(sender, instance, created, **kwargs):
    #basic signal for storing the latest month 
    #actually not needed,but just trying signals 
    payroll_data=get_object_or_404(latestmonth,id=1)
    payroll_data.month=instance.month
    payroll_data.save()