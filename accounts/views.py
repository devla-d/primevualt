from django.shortcuts import render,redirect
from django.contrib import  messages
from .models import Account,Coupon
from .forms import RegistrationForm,ProfileUpdateForm
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.decorators import login_required





def register(request,*args, **kwargs):
    code = str(kwargs.get('ref_slug'))
    try:
        profile = Account.objects.get(slug= code)
        request.session['ref_profile'] = profile.id 
    except:
        pass
    user= request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        profile_id =  request.session.get('ref_profile')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if profile_id is not None:
                recom_by = Account.objects.get(id=profile_id)
                recom_by.refferal += 1
                recom_by.save()
                code = form.cleaned_data['coupon']
                c = Coupon.objects.filter(code=code)[0]
                c.active = False
                c.save()
                form.save()
                messages.success(request, f'Account created !')
                return redirect('login')
            else:
                code = form.cleaned_data['coupon']
                c = Coupon.objects.filter(code=code)[0]
                c.active = False
                c.save()
                form.save()
                messages.success(request, f'Account created !')
                return redirect('login')       
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def LogoutView(request):
    logout(request)
    return redirect('login')





@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account updated !')
            return redirect('account')
    else:
        form = ProfileUpdateForm()
    return render(request , 'profile.html', {"form":form})



















