from django.shortcuts import render
import smtplib
from pandas import read_excel
from django.contrib.auth import get_user_model
import random
#email part
SenderAddress="bandersnatch28@gmail.com"
pswd="--__--"
# password generator.
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']   
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']        


def homepage(request):
    data=read_excel("D:\\web\\employee.xlsx")
    # mobile=[];name=[];email=[]
    context={}
    User = get_user_model()
    for i in range(len(data)):
        username=data["Name"][i]
        email=data["email"][i]
        password=""
        for _ in range(2):
            password+=random.choice(DIGITS)+random.choice(LOCASE_CHARACTERS)+random.choice(UPCASE_CHARACTERS)
          
        # mobile.append(data["mobile"][i]);name.append(data["Name"][i]);email.append(data["email"][i])
        User.objects.get_or_create(username=username, is_staff=False) 
        u = User.objects.get(username=username)   
        u.set_password(password)
        u.email=email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SenderAddress, pswd)
        msg = "hello :) below are the credentials that you need to check your payroll details"+"\n"+"your username is:\t"+username+"\nyour password is:\t"+password+"\n link to the website:\t amithnc.pythonanywhere.com/moniter"+"\n\n"+"NOTE:please change your  password once u login\n"+"\n\n"+"-technical team @NCA"
        subject = "Payroll login credentials"
        body = "Subject: {}\n\n{}".format(subject,msg)
        server.sendmail(SenderAddress, email, body)
        print("created and mail sent to",username)
        u.save()
    server.quit()   
    # context['mainlist']=zip(name,mobile,email)
    return render(request,'home.html',context)