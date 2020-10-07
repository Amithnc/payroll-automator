from django.urls import path
from . import views
urlpatterns = [
    path('create-employee/<int:id>',views.createuser),
    path('update-details/<int:id>/',views.updatedetails,name='update-details'),
    path('verify-employee/<int:id>/',views.verifyemployee)
]