from django.shortcuts import render, redirect
from django.contrib import messages
from home.models import User_Registration, User_Expense, Total_Income

# Create your views here.


def value_check(value):
    return value is None or value == ""


def user_exist(username, password):
    user = User_Registration.objects.filter(
        username=username, password=password).first()
    return user


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

        if not user_exist(username, password):
            User_Registration.objects.create(
                username=username, password=password)
            messages.success(request, "user register successfully")
            return redirect("/")
        else:
            messages.warning(request, "user already exist")
            return redirect("/")
    return render(request,"")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if value_check(username):
            messages.warning(request, "please enter the username")
            return redirect("/")

        if value_check(password):
            messages.warning(request, "please enter the username")
            return redirect("/")

        user = user_exist(username, password)
        if not user:
            messages.warning(request, "user not register")
            return redirect("/")
        else:
            request.session['user_id'] = user.id
            messages.success(request, "user logged in successfully")
            return redirect("/")
    return render(request,"")


def create_expense(request):
    id = request.session.get('user_id')
    expense_type;
    if not id:
        messages.warning(request, "user not found please login again")
        return redirect("/")

    user = User_Registration.objects.filter(id=id).first()
    if not user:
        messages.warning(request, "user not found please login again")
        return redirect("/")

    if request.method == "POST":
        expense_name=request.POST.get("expensename")
        amount=request.POST.get("amount")
        if value_check(expense_name):
            messages.warning(request, "please enter the expense name")
            return redirect("/")
         
        if value_check(amount):
            messages.warning(request, "please enter the amount")
            return redirect("/")
        
        if int(amount)< 0 :
            expense_type="Debit"
        else:
            expense_type="Credit"
        
        
        
        User_Expense.objects.create(expense_name=expense_name,expense_type=expense_type,user=id)