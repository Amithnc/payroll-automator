from django.db import models

# Create your models here.
class employee(models.Model):
    employee_name=models.CharField(max_length=30,default='',help_text="enter the employee name")
    employee_mob=models.CharField(max_length=15,default='',help_text="enter the mobile number")
    employee_email=models.CharField(max_length=30,default='',help_text="enter the email id")

    def __str__(self):
        return str(self.employee_name) 