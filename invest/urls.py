from django.urls import path,include
from . import views  
from .views import (
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path('task/', views.home, name="home"),
    path('vendors/', views.approved_vendors, name="vendors"),
    path('admin/dashboard/newpost/', views.newpost, name="newpost"),
    path('search/', views.SearchView.as_view(), name='search' ),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('admin/dashboard/', views.dashboard, name="dashboard"),
    path('admin/dashboard/users/', views.users, name="dashboard-users"),
    path('admin/dashboard/withdraw/', views.withdraw, name="dashboard-withdraw"),
    path('admin/dashboard/coupon/', views.coupon, name="dashboard-coupon"),
    path('admin/dashboard/payments/', views.payment, name="dashboard-payment"),
    path('admin/dashboard/vendors/', views.vendors, name="dashboard-vendor"),
    path('account/', views.account, name="account"),
    #path('investment/pay', views.invest_pay, name="invest_pay"),
   
]