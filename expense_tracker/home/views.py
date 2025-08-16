from django.shortcuts import render,redirect
from django.contrib import messages
from home.models import User_Registration,User_Expense,Total_Income

# Create your views here.

def value_check(value):
    return value is None or value == ""

def user_exist(username,password):
    user=User_Registration.objects.filter(username=username,password=password).first()
    return 

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if value_check(username):
            messages.warning(request, "please enter the username")
            return redirect("/")
        
        if value_check(password):
            messages.warning(request, "please enter the username")
            return redirect("/")
            
        if not user_exist(username,password):
            User_Registration.objects.create(username=username,password=password)