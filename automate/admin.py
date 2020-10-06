from django.contrib import admin
from .models import employee
# Register your models here.
admin.site.index_title=""
admin.site.site_title="payroll_automator | Automation of payroll process"
admin.site.site_header="Admin Portal (PAYROLL AUTOMATOR)" 

class employeeAdmin(admin.ModelAdmin):
    list_display = ('id','employee_file',)

admin.site.register(employee,employeeAdmin)