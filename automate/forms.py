from django import forms  
from .models import employee,payroll 
from pandas import read_excel
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
class registerForm(forms.ModelForm):  
    class Meta:  
        model = employee  

        fields = ('employee_file',)  
        help_texts = {
            'employee_file': '',
        }
    def clean(self):    
        employee_file=self.cleaned_data['employee_file'] 
        check_file_name=str(employee_file)
        check_file_name=check_file_name.split('/')
        check_file_extension=str(employee_file)
        check_file_extension=check_file_extension.split('.')
        if check_file_extension[1] !="xlsx" and check_file_extension!="xlsm" and check_file_extension!="xlx" :
            raise forms.ValidationError("unsupported file format ,supported file formats are xlsx,xlsm,xlx")
        if check_file_name[0]=='file':
            raise forms.ValidationError("No file selected please upload appropriate file")
        data=read_excel(employee_file)  
        for i in range(len(data)):
            try:
                email=data["email"][i]
            except:
                raise ValidationError("Invalid file or Invaid file content please make sure the file is employee-file ")    
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError("wrong email format for user name "+data['Name'][i]+" at row number "+str(i+2))   
        return self.cleaned_data

class registerFormnovalidate(forms.ModelForm):  
    class Meta:  
        model = employee  
        fields = ('employee_file',)  
        help_texts = {
            'employee_file': '',
        }  

class payrollUpdateForm(forms.ModelForm):
    class Meta:  
        model = payroll  

        fields = ('payroll_file','status')  
        help_texts = {
            'payroll_file': '',
        }
    def clean(self):
        payroll_file=self.cleaned_data['payroll_file'] 
        check_file_name=str(payroll_file)
        check_file_name=check_file_name.split('/')
        if check_file_name[0]=='file':
            raise forms.ValidationError("No file selected please upload appropriate file")

        return self.cleaned_data

class NoValidatePayroll(forms.ModelForm):  
    class Meta:  
        model = payroll  
        fields = ('payroll_file','status')  
        help_texts = {
            'payroll_file': '',
        }  