from django.db import models
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time
from django import forms  
from pandas import read_excel
from django.core.exceptions import ValidationError




class employee(models.Model):
    employee_file=models.FileField(upload_to='file',help_text="please upload file",verbose_name='employee details')
    
    def __str__(self):
        return str(self.employee_file) 



class payroll(models.Model):
    status_option= [
            ('Visible', 'visible'),
            ('Hide', 'hide')
    ]
    # month=[
    #     ('January','January'),
    #     ('February','February'),
    #     ('March','March'),
    #     ('April','April'),
    #     ('May','May'),
    #     ('June','June'),
    #     ('July','July'),
    #     ('August','August'),
    #     ('September','September'),
    #     ('October','October'),
    #     ('November','November'),
    #     ('December','December'),
    # ]
    status=models.CharField(choices=status_option,help_text="please select one option",max_length=10,default='')
    payroll_file=models.FileField(upload_to='file',help_text="please upload file",verbose_name='payroll details')
    month=models.CharField(help_text="please select the month",max_length=20,default='',blank=True,editable=False)

    def clean(self):
        check_file_extension=str(self.payroll_file)
        check_file_extension=check_file_extension.split('.')
        if check_file_extension[1] !="xlsx" and check_file_extension!="xlsm" and check_file_extension!="xlx" :
            raise forms.ValidationError("unsupported file format ,supported file formats are xlsx,xlsm,xlx")
        data=read_excel(self.payroll_file)
        try:
            month=data['Month'][0]
        except:
            raise ValidationError("Invalid file or Invaid file content please make sure the file is payroll-file ")    

    def save(self, *args, **kwargs):
        data=read_excel(self.payroll_file)
        self.month=data['Month'][0]
        time.sleep(5)  
        super(payroll, self).save(*args, **kwargs)



    def __str__(self):
        return str(self.month) 