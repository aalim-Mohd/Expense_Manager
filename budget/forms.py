from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from budget.models import Category,Transactions
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CategoryForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):

        self.user=kwargs.pop("user")

        return super().__init__(*args,**kwargs)
    
    class Meta:

        model=Category

        fields=["name","budget","image"]

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),

            "budget":forms.NumberInput(attrs={"class":"form-control"}),

            "image":forms.FileInput(attrs={"class":"form-control"}),
            
        }

    def clean(self):
        self.cleaned_data=super().clean()

        budget_amount=int(self.cleaned_data.get("budget"))

        print(self.user,"inside c form")

        if budget_amount<100:

            self.add_error("budget","budget amount < 100")

        category_name=self.cleaned_data.get("name")

        owner=self.user

        if not self.instance.pk:

            print("updating",self.instance.pk)

            is_exist=Category.objects.filter(name=category_name,owner=owner).exists()
        
            if is_exist:
                self.add_error("name","category with this name already exist!")
            
        else:
            is_exist=Category.objects.filter(name=category_name,owner=owner).exclude(pk=self.instance.pk).exists()
            if is_exist:
                self.add_error("name","category with this name already exist!")
        return self.cleaned_data

class TransactionForm(forms.ModelForm):

    class Meta:

        model=Transactions

        fields=["title","amount","category_obj","payment_method"]

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),

            "amount":forms.NumberInput(attrs={"class":"form-control mb-2"}),

            "category_obj":forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "payment_method":forms.Select(attrs={"Class":"form-control form-select mb-2"}),

        
        }

class TransactionFilterForm(forms.Form):

    start_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))

    end_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))

class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"})),

    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={

            "username":forms.TextInput(attrs={"class":"form-control mb-2"}),

            "email":forms.EmailInput(attrs={"class":"form-control mb-2"}),


        }

class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    