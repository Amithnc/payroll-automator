from django.shortcuts import render,get_object_or_404,redirect
import smtplib
from django.contrib import auth
from pandas import read_excel
from django.contrib.auth import get_user_model
import random
from .models import employee,payroll
from .forms import registerForm,registerFormnovalidate
from django.contrib import messages
import time
from django.contrib.auth.decorators import login_required
#email part
SenderAddress="bandersnatch28@gmail.com"
pswd="--__--"
# password generator.
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']   
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']        

@login_required(login_url='/login')
def homepage(request):
    files=employee.objects.all()
    payroll_files=payroll.objects.all()
    return_resposne={};return_resposne['files']=files
    return_resposne['payroll_file']=payroll_files
    return render(request,'home.html',return_resposne)

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/login')
def createuser(request,id):
    instance=get_object_or_404(employee,id=id) 
    filename=instance.employee_file
    data=read_excel(filename)
    User = get_user_model()
    count=0
    for i in range(len(data)):
        username=data["Name"][i]   
        if User.objects.filter(username=username).exists():
            continue
        else:
            email=data["email"][i]
            password=""
            for _ in range(2):
                password+=random.choice(DIGITS)+random.choice(LOCASE_CHARACTERS)+random.choice(UPCASE_CHARACTERS)
            User.objects.get_or_create(username=username, is_staff=True) 
            u = User.objects.get(username=username)   #
            u.set_password(password)
            u.email=email
            # server = smtplib.SMTP("smtp.gmail.com", 587)
            # server.starttls()
            # server.login(SenderAddress, pswd)
            # msg = "hello" + username +"below are the credentials that you need to check your payroll details"+"\n"+"your username is:\t"+username+"\nyour password is:\t"+password+"\n link to the website:\t http://127.0.0.1:8000/"+"\n\n"+"NOTE:please change your  password once u login\n"+"\n\n"+"-technical team @NCA"
            # subject = "Payroll login credentials"
            # body = "Subject: {}\n\n{}".format(subject,msg)
            # server.sendmail(SenderAddress, email, body)
            count+=1
            u.save()
        # server.quit()   
    messages.success(request, 'created '+str(count)+' users successfully')    
    url="/verify-employee/"+str(id)
    return redirect(url) 

@login_required(login_url='/login')
def verifyemployee(request,id):
    instance=get_object_or_404(employee,id=id) 
    filename=instance.employee_file
    data=read_excel(filename)
    name=[];email=[];status=[];context={};flag=0
    User = get_user_model()
    for i in range(len(data)):
        if User.objects.filter(username=data["Name"][i]).exists():
            status.append(0)
        else:
            status.append(1)    
        name.append(data["Name"][i]);email.append(data["email"][i])
    if status.count(1)==0:
        flag=1   
    context['mainlist']=zip(name,email,status)
    context['flag']=flag
    context['id']=instance.id
    return render(request,'verifyemployee.html',context)

@login_required(login_url='/login')
def updatedetails(request,id):
    instance = get_object_or_404(employee,id=id)  
    if request.method == "POST":
        form = registerForm(request.POST  or None,files=request.FILES,instance = instance)
        if form.is_valid():
            temp=form.save(commit=False)
            time.sleep(3)    
            temp.save()
            url="/verify-employee/"+str(id)
            messages.success(request, 'File Uploaded Successfully')
            return redirect(url)
    else:
        form = registerFormnovalidate(request.POST  or None,files=request.FILES,instance = instance)        
    return_resposne={}
    return_resposne['instance']=instance  
    return_resposne['form']=form  
    return_resposne['url_name']='update-details'
    return render(request,'update.html',return_resposne)   