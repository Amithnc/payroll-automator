from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from . import views
urlpatterns = [
    path('',views.homepage),
    path('login/',
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'site_header': 'Login to payroll-portal',
                'site_title' : 'payroll-Portal',
            })),
    path('logout/',views.logout),
    path('create-employee/<int:id>/',views.createuser),
    path('update-details/<int:id>/',views.updatedetails,name='update-details'),
    path('verify-employee/<int:id>/',views.verifyemployee),
    path('update-payroll/<int:id>/',views.update_payroll,name='update-payroll'),
    
]