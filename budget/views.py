from django.shortcuts import render,redirect
from django.views.generic import View
from budget.forms import CategoryForm,TransactionForm,TransactionFilterForm,RegistrationForm,LoginForm
from budget.models import Category,Transactions
from django.utils import timezone
from django.db.models import Sum #Avg,Count,Min,Max
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.messages import success,error
from budget.decorators import signin_required
from django.utils.decorators import method_decorator

# function_dec => method_deco dispatch

# @method_decorator(signin_required,name="dispatch")

@method_decorator(signin_required,name="dispatch")

class CategoryCreateView(View):  

    def get(self,request,*args,**kwargs):


        form_instance=CategoryForm(user=request.user)

        qs=Category.objects.filter(owner=request.user)

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self,request,*args,**kwargs):



        form_instance=CategoryForm(request.POST,user=request.user,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("category-add")
        
        else:

            return render(request,"category_add.html",{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")      

class CategoryEditView(View):
#url:localhost:8000/category/{int:pk}/edit/

    def get(self,request,*args,**kwargs):

        

        id=kwargs.get("pk")

        category_obj=Category.objects.get(id=id)

        form_instance=CategoryForm(instance=category_obj)

        return render(request,"category_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        category_obj=Category.objects.get(id=id)

        form_instance=CategoryForm(request.POST,instance=category_obj)

        if form_instance.is_valid():
            
            form_instance.save()

            return redirect("category-add")
        
        else:
            return render(request,"category_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")

class CategoryDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Category.objects.get(id=id).delete()

        return redirect("category-add")

@method_decorator(signin_required,name="dispatch")

class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionForm()

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        categories=Category.objects.filter(owner=request.user)

        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)

        return render(request,"transaction_add.html",{"form":form_instance,"transactions":qs,"categories":categories})
    
    def post(self,request,*args,**kwargs):

        form_instance=TransactionForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("transactions-add")
        
        else:
             return render(request,"transaction_add.html",{"form":form_instance})

#url:localhost:8000/transaction/<int:pk>/edit/

@method_decorator(signin_required,name="dispatch")

class TransactionUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        trans_obj=Transactions.objects.get(id=id)

        form_instance=TransactionForm(instance=trans_obj)

        return render(request,"transaction_edit.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        
        trans_obj=Transactions.objects.get(id=id)

        form_instance=TransactionForm(request.POST,instance=trans_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("transactions-add")
        
        else:
            return render(request,"transaction_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")

class TransactionDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Transactions.objects.get(id=id).delete()

        return redirect("transactions-add")

@method_decorator(signin_required,name="dispatch")

class ExpenseSummaryView(View):
    
    def get(self,request,*args,**kwargs):

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year)
        
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))

        category_summary=qs.values("category_obj__name").annotate(total=Sum("amount"))

        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))

        data={
            "total_expense":total_expense.get("total"),

            "category_summary":category_summary,

            "payment_summary":payment_summary,
        }
        
        return render(request,"expense_summary.html",data)
        
@method_decorator(signin_required,name="dispatch")

class TransactionSummaryView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionFilterForm()

        current_month=timezone.now().month

        current_year=timezone.now().year


        if 'start_date' in request.GET and 'end_date' in request.GET:

            st_date=request.GET.get("start_date")

            en_date=request.GET.get("end_date")

            qs=Transactions.objects.filter(

                                            created_date__gte=st_date,
                                            created_date__lte=en_date

                                            )

        else:


            qs=Transactions.objects.filter(

                                        created_date__month=current_month,
                                        created_date__year=current_year

                                        )
        
        return render(request,"transaction_summary.html",{"transactions":qs,"form":form_instance})

        
class ChartView(View):

    
    def get(self,request,*args,**kwargs):

        return render(request,"chart.html")
    
class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"Account created successfully!")

            print("Account created successfully!")

            return redirect("signup")
        
        else:
            print("Failed to Create Account!")

            messages.error(request,"Failed to create an account!")

            return render(request,"register.html",{"form":form_instance})

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form__instance=LoginForm(request.POST)

        if form__instance.is_valid():
           
            data=form__instance.cleaned_data

            user_obj=authenticate(request,**data)

            if user_obj:

                login(request,user_obj)

                messages.success(request,"Login success!")

                return redirect("expense-summary")
        
        else:

            messages.error(request,"Failed to login to your account!")

            return render(request,"login.html",{"form":form__instance})

@method_decorator(signin_required,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")