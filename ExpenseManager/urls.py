"""
URL configuration for ExpenseManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from budget import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/add/',views.CategoryCreateView.as_view(),name="category-add"),
    path('category/<int:pk>/edit/',views.CategoryEditView.as_view(),name="category-edit"),
    path('category/<int:pk>/delete/',views.CategoryDeleteView.as_view(),name="category-delete"),
    path('transaction/add/',views.TransactionCreateView.as_view(),name="transactions-add"),
    path('transaction/<int:pk>/edit/',views.TransactionUpdateView.as_view(),name="transaction-edit"),
    path('transaction/<int:pk>/delete/',views.TransactionDeleteView.as_view(),name="transaction-delete"),
    path('transaction/summary/',views.TransactionSummaryView.as_view(),name="transaction-summary"),
    path('expense/summary/',views.ExpenseSummaryView.as_view(),name="expense-summary"),
    path('expense/chart/',views.ChartView.as_view(),name="expense-chart"),
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name="signin"),
    path('signout/',views.SignOutView.as_view(),name="signout"),

    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
