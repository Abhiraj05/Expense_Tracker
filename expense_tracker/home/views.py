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


def user_expense(id):
    userex = User_Expense.objects.filter(user=id).first()
    return userex


def user_income(id):
    userin = Total_Income.objects.filter(
        user=id).first()
    return userin


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
    return render(request, "signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if value_check(username):
            messages.warning(request, "please enter the username")
            return redirect("/login/")

        if value_check(password):
            messages.warning(request, "please enter the username")
            return redirect("/login/")

        user = user_exist(username, password)
        if not user:
            messages.warning(request, "user not register")
            return redirect("/login/")
        else:
            request.session['user_id'] = user.id
            messages.success(request, "user logged in successfully")
            return redirect("/user-expense/")
    return render(request, "signin.html")


def create_expense(request):
    user_id = request.session.get('user_id')
    total_amount = 0
    cal_credit_amount = 0
    cal_debit_amount = 0
    expense_type = "Debit"
    user_expense_records = ''
    if not user_id:
        messages.warning(request, "user not found please login again")
        return redirect("/login/")

    user = User_Registration.objects.filter(id=user_id).first()
    if not user:
        messages.warning(request, "user not found please login again")
        return redirect("/login/")

    # if not user_expense(user_id):
    #         messages.warning(request, "no record found")

    if user_expense(user_id):
        user_expense_records = User_Expense.objects.filter(
            user=user_id).all()

    if request.method == "POST":
        expense_name = request.POST.get("expensename")
        amount = request.POST.get("amount")

        if value_check(expense_name):
            messages.warning(request, "please enter the expense name")
            return redirect("/user-expense/")

        if value_check(amount):
            messages.warning(request, "please enter the amount")
            return redirect("/user-expense/")

        if int(amount) < 0:
            expense_type = "Debit"
        else:
            expense_type = "Credit"

        user_instance = User_Registration.objects.filter(id=user_id).first()
        if not user_instance:
            messages.warning(request, "no record found")
            return redirect("/user-expense/")

        if user_instance:
            User_Expense.objects.create(
                expense_name=expense_name, expense_type=expense_type, amount=amount, user=user_instance)
            messages.success(request, "expense created successfully")

        if user_expense(user_id):
            user_expense_records = User_Expense.objects.filter(
                user=user_id).all()

        for expense in user_expense_records:
            if expense.expense_type == "Credit":
               cal_credit_amount += int(expense.amount)
            else:
                cal_debit_amount -= int(expense.amount)
        
        
        total_amount = cal_credit_amount-cal_debit_amount

        user_total_income = user_income(user_id)
        if not user_total_income:
            user_instance = User_Registration.objects.filter(
                id=user_id).first()
            Total_Income.objects.create(
                user=user_instance, total_income=total_amount,credit_amount=cal_credit_amount,debit_amount=cal_debit_amount)
        else:
            income_instance = user_total_income
            income_instance.total_income = total_amount
            income_instance.credit_amount=cal_credit_amount
            income_instance.debit_amount=cal_debit_amount
            income_instance.save()

        return redirect("/user-expense/")
    
    income=user_income(user_id)

    context = {"user":user.username,"all_expenses": user_expense_records,
               "total_amount": income}
    return render(request, "main.html", context)


def delete_task(request, expense_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "user not found please login again")
        return redirect("/login/")
    
    if user_income(user_id):
        user_total_income = user_income(user_id)
        debited_amount=User_Expense.objects.filter(id=expense_id, user=user_id).first()
        total =user_total_income.total_income - debited_amount.amount
        if debited_amount.expense_type=="Credit":
            camount=user_total_income.credit_amount-debited_amount.amount
            user_total_income.credit_amount=camount
        else:
            damount=user_total_income.debit_amount+debited_amount.amount
            user_total_income.debit_amount=damount
            
        user_total_income.total_income=total
        user_total_income.save()
       
    User_Expense.objects.filter(id=expense_id, user=user_id).delete()
    
    if not user_expense(user_id):
        user_total_income = user_income(user_id)
        user_total_income.total_income = 0
        user_total_income.credit_amount = 0
        user_total_income.debit_amount = 0
        
        user_total_income.save()
    messages.success(request, "expense deleted successfully")
    return redirect("/user-expense/")

def logout(request):
    request.session.flush()
    return redirect('/login/')