from django.contrib import admin
from .models import employee,payroll,latestmonth

# Register your models here.
admin.site.index_title=""
admin.site.site_title="payroll_automator | Automation of payroll process"
admin.site.site_header="Admin Portal (PAYROLL AUTOMATOR)" 

class employeeAdmin(admin.ModelAdmin):
    list_display = ('id','employee_file',)

admin.site.register(employee,employeeAdmin)

class payrollAdmin(admin.ModelAdmin):
    list_display=('month','payroll_file','status')

admin.site.register(payroll,payrollAdmin)    

class latestmonthAdmin(admin.ModelAdmin):
    list_display=('month','date_time')

admin.site.register(latestmonth,latestmonthAdmin) 
