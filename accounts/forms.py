from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account,Coupon,Vendor


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    fullname = forms.CharField(max_length=200)
  


    class Meta:
        model = Account
        fields = ["fullname","username","coupon","email","country"]

    def clean(self):
        coupon = self.cleaned_data['coupon']
        try:
            code = Coupon.objects.get(code=coupon,active=True)
        except Coupon.DoesNotExist:
            raise forms.ValidationError("coupon does not exist")

        if  Account.objects.filter(coupon=coupon).exists():
            raise forms.ValidationError("coupon is already  used")

        if code.active == False:
            raise forms.ValidationError("coupon is expired  ")


        
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ["fullname","username","email","profile_image"]



class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ["user", "whatsapp"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Account.objects.all()






 


    
     

