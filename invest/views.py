from django.shortcuts import render,redirect
from django.contrib import  messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .decorators import manager_required
from .models import *
from accounts.models import Account,Coupon,Vendor
from .forms  import PostForm
from django.utils import  timezone
from accounts.forms import VendorForm

def home(request):
   
    obj  = Post.objects.all()
    paginator = Paginator(obj, 15) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return  render(request, "task.html", {"posts":posts})

def landingpage(request):
    return render(request, 'home.html')


@manager_required
def dashboard(request):
    
    context = {
        "pending_payment": Payment.objects.filter(status="PENDING").count(),
        "payment": Payment.objects.filter(status="COMPLETED").count(),
        "account" : Account.objects.all().count(),
        "withdraw" : Withdraw.objects.filter(status="COMPLETED").count(),
        "pending_withdraw": Withdraw.objects.filter(status="PENDING").count()

    }
    return render(request, 'admin/dashboard.html', context)


@manager_required
def users(request):
    context = {
        "accounts" : Account.objects.all()

    }
    return render(request, 'admin/users.html', context)




@manager_required
def withdraw(request):
    context = {
        "withdraws" : Withdraw.objects.all()

    }
    return render(request, 'admin/withdraw.html', context)


@manager_required
def vendors(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard-vendor')
            messages.success(request , f"Vendor added")
    else:
        context = {
            "vendors" : Vendor.objects.all(),
            "form" : VendorForm()

        }
        return render(request, 'admin/vendorlist.html', context)



def rand_code():
    code =  str(uuid.uuid4()).replace("-", "")[:10]
    return code

@manager_required
def coupon(request):
    if request.method == 'POST':
        package = request.POST['package']
        price = request.POST['price']
        coupon = Coupon.objects.create(
            price = price,
            package =package,
            code =rand_code()
        )
        return redirect('dashboard-coupon')


    obj  = Coupon.objects.all()
    paginator = Paginator(obj, 30) 
    page_number = request.GET.get('page')
    coupons = paginator.get_page(page_number)
    return render(request, 'admin/coupon.html', {"coupons":coupons})



@manager_required
def payment(request):
    context = {
        "payments" : Payment.objects.all()

    }
    return render(request, 'admin/payment.html', context)

@manager_required    
@login_required
def newpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request , f"Post created succesfully")
            return redirect('newpost')
    form = PostForm()
    return render(request, "admin/newpost.html", {"form":form})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'postdetail.html', {'post': post})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','category', 'content']
    template_name = 'newpost.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False






class SearchView(ListView):
    model = Post
    template_name = 'task.html'
    context_object_name = 'posts'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query)
        )
        return object_list


@login_required
def account(request):
    if request.method == 'POST':
        amount =float(request.POST['amount'])
        user = request.user
        time = timezone.now()
        if amount > float(user.total_earnings):
            messages.info(request , f"sorry you dont have enough found to withdraw")
            return redirect("account")
        else:   
            withdraw = Withdraw.objects.create(
                user= user,
                time= time,
                status = 'PENDING',
                amount = amount
            )
            return redirect("account")
    pay= Payment.objects.filter(user = request.user)
    withdraw = Withdraw.objects.filter(user=request.user)
    
    context = {
        "pay": pay,
        "withdraws": withdraw
    }
    return render(request, 'account.html', context)




def approved_vendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor.html',{"vendors":vendors})