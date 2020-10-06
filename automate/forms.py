from django import forms  
from .models import employee  
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
        data=read_excel(employee_file)  
        for i in range(len(data)):
            email=data["email"][i]
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError("wrong email format for user name "+data['Name'][i]+" at row number "+str(i+1))   
        return self.cleaned_data

class registerFormnovalidate(forms.ModelForm):  
    class Meta:  
        model = employee  
        fields = ('employee_file',)  
        help_texts = {
            'employee_file': '',
        }  