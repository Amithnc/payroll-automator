from django.shortcuts import render,get_object_or_404,redirect
import smtplib
from django.contrib import auth
from pandas import read_excel
import pandas as pd
from django.contrib.auth import get_user_model
import random
from .models import employee,payroll
from .forms import registerForm,registerFormnovalidate #payrollUpdateForm,NoValidatePayroll
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML 
import tempfile

from xhtml2pdf import pisa
import requests

#email part
SenderAddress="bandersnatch28@gmail.com"
pswd="Geetha10raksha1234"
# password generator.
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']   
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']        

@login_required(login_url='/login')
def homepage(request):
    if(request.user.is_superuser):
        files=employee.objects.all()
        payroll_files=payroll.objects.all()
        return_resposne={};return_resposne['files']=files
        return_resposne['payroll_file']=payroll_files
        return render(request,'home.html',return_resposne)
    else:
        TA=[];DA=[];PF=[];basic=[];total=[];month=[];context={}
        files=payroll.objects.all()
        for File in files:
            if File.status =="Visible":
                data=read_excel(File.payroll_file)
                for i in range(len(data)):
                    if str(request.user) == str(data["Name"][i]):
                        print(data["visibility"][i])
                        if data["visibility"][i]=="yes":
                            ph_number=(data["Phone number"][i])
                            TA.append(data["TA"][i])
                            DA.append(data["DA"][i])
                            PF.append(data["PF"][i])
                            basic.append(data["Basic"][i])
                            total.append(data["amount"][i])
                            month.append(data['Month'][0])
                            context['list']=zip(TA,DA,PF,basic,total,month)
                            context['ph_number']=ph_number
                            return render(request,'home.html',context)
                        else:
                            continue    
                else:
                    return render(request,'home.html',context)
            else:
                    return render(request,'home.html',context)        


# def pdfview(request):
#     response= HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment;filename="home.pdf"'
#     response['Content-Transfer-Encoding']= 'binary'
#     html_string=render_to_string('templates/pdfoutput.html',{'expenses':[],})
#     html=HTML(string=html_string)
#     result=html.write_pdf()
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output=open(output.name,'rb')
#         response.write(output.read())
#     return response


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
            u = User.objects.get(username=username)   
            u.set_password(password)
            u.email=email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SenderAddress, pswd)
            print('3')
            msg = "hello " + username +" below are the credentials that you need to check your payroll details"+"\n"+"your username is:\t"+username+"\nyour password is:\t"+password+"\n link to the website:\t http://127.0.0.1:8000/"+"\n\n"+"NOTE:please change your  password once u login\n"+"\n\n"+"-technical team @Payroll-Automator"
            subject = "Payroll login credentials"
            body = "Subject: {}\n\n{}".format(subject,msg)
            server.sendmail(SenderAddress, email, body)
            count+=1
            u.save()
        server.quit()   
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

#for payroll model
# @login_required(login_url='/login')
# def update_payroll(request,id):
#     instance=get_object_or_404(payroll,id=id)
#     if request.method=="POST":
#         form=payrollUpdateForm(request.POST or None,files=request.FILES,instance=instance)
#         if form.is_valid():
#             temp=form.save(commit=False)
#             temp.save()
#             url="/verify-payroll"+str(id)
#             messages.success(request,'File Uploaded Successfully')
#             return redirect('/')
#     else:
#         form = NoValidatePayroll(request.POST  or None,files=request.FILES,instance = instance)
#     return_resposne={}
#     return_resposne['instance']=instance  
#     return_resposne['form']=form  
#     return_resposne['url_name']='update-payroll'
#     return render(request,'update.html',return_resposne)

@login_required(login_url='/login')
def verifypayroll(request,id):
    instance=get_object_or_404(payroll,id=id) 
    filename=instance.payroll_file
    data=read_excel(filename)
    name=[];phone=[];amount=[];status=[];context={};flag=0
    for i in range(len(data)):
        status.append(data['status'][i])
        name.append(data['Name'][i]);phone.append(data['Phone number'][i]);amount.append(data['amount'][i])    
    if(status.count("Not Sent"))==0:
        flag=1
    context['mainlist']=zip(name,phone,amount,status)
    context['flag']=flag
    context['id']=instance.id
    context['month']=instance.month
    return render(request,'verifypayroll.html',context)

def sendmessage(request,id):
    instance=get_object_or_404(payroll,id=id)
    filename=instance.payroll_file
    data=read_excel(filename)
    month=instance.month

    #to update the status 
    from openpyxl import load_workbook 
    wb = load_workbook(filename =filename)
    ws1 = wb.active
    for i in range(len(data)):
        url = "https://www.fast2sms.com/dev/bulk"
        s1= "sender_id=FSTSMS&language=english&route=qt&numbers="
        v1=str(data["Phone number"][i])
        s2="&message=37272&variables={#DD#}|{#AA#}|{#BB#}&variables_values="
        values=[data["Name"][i],str(data["amount"][i]),month]
        s3="|".join(values)
        payload=s1+v1+s2+s3
        headers = {
            'authorization': "ikvTwZbp4tSNDdmI1Ls8BjcFehOVAqglozuKQYMrUHaCn7R6G2atl7ZjPgYDkvNoMEueA32d6ws85O1C",
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        ws1["I"+str(i+2)].value="Sent"
    wb.save("D:\\project\\payroll-automator\\media\\"+str(filename))
    wb.close()
    url="/verify-payroll/"+str(id)
    messages.success(request, 'successfully sent messages')
    return redirect(url) 