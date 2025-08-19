from django.db import models

# Create your models here.


class User_Registration(models.Model):
    username = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=10, blank=False, null=False)



class User_Expense(models.Model):
    expense_name = models.CharField(max_length=100, blank=False, null=False)
    expense_type = models.CharField(max_length=100, choices=(
        ("Credit", "Credit"),
        ("Debit", "Debit")), default="Debit")
    amount= models.IntegerField(default=0)
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)





class Total_Income(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE)
    total_income = models.IntegerField(default=0)
    credit_amount = models.IntegerField(default=0)
    debit_amount = models.IntegerField(default=0)
    
    
    