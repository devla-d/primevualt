from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
import random
import string
from django.utils import timezone

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))





class Coupon(models.Model):
    PRICE = (
        ("3,000", "3,000"),
        ("5,000", "5,000"),
        ("10,000", "10,000"),
        ("20,000", "20,000"),
        ("50,000", "50,000"),
        ("100,000", "100,000")
    
    )
    PACKAGE = (
        ("Bigginer", "Bigginer"),
        ("Standard", "Standard"),
        ("Platinum", "Platinum"),
        ("Ruby", "Ruby"),
        ("Gold", "Gold"),
        ("Eminent", "Eminent")
    
    )
    code = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    price = models.IntegerField(null =True, blank=True)
    package = models.CharField(null =True, blank=True, max_length=50, choices=PACKAGE)

    class Meta:
            ordering = ('-created',"active")

    def __str__(self):
        return f"Coupon :{self.code}"


class Vendor(models.Model):
    user = models.ForeignKey('Account', on_delete=models.CASCADE)
    whatsapp = models.CharField(max_length=100)

    def __str__(self):
        return self.whatsapp






















class MyAccountManager(BaseUserManager):
    def create_user(self,username, email, password=None):
        if not email:
            raise ValueError('email is required')
        if not username:
            raise ValueError('username is required')
        
        user = self.model(
            email= self.normalize_email(email),
            username= username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email,password):
        user = self.create_user(
             email= self.normalize_email(email),
            username= username,
            password= password,
        
        )
        user.is_admin=True
        user.is_superuser=True
        user.is_staff= True
        user.save(using=self._db)
        return user








class Account(AbstractBaseUser):
    COUNTRY = (
        ("NIGERIA", "NIGERIA"),
        ("GHANA", "GHANA"),
        ("UGANDA", "UGANDA"),
        ("SOUTH AFRICA", "SOUTH AFRICA"),
        ("KENYA", "KENYA")
    )
    fullname =  models.CharField(max_length=30, blank= True, null=True)
    email       = models.EmailField(verbose_name='email', max_length=60, unique=True )
    username    = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login  = models.DateTimeField(verbose_name='last login', auto_now=True)
    country =  models.CharField(max_length=30,choices= COUNTRY)
    phone_number =  models.IntegerField( blank= True, null=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    profile_image = models.ImageField(blank=True, null=True, default='teamwork.png', upload_to='profile')
    refferal = models.IntegerField(default=0)
    balance = models.FloatField(default=0)
    investment_amount = models.FloatField(default=0)
    withdraw_amount = models.FloatField(default=0)
    total_earnings = models.FloatField(default=0)
    slug = models.SlugField(null=True, blank=True)
    coupon = models.CharField(unique=True, max_length=50)
  


    
    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def  has_module_perms(self, app_label):
        return True
     

    def total_ref_ernings(self):
        code = self.coupon
        cde = Coupon.objects.get(code=code)
        ref_balance = float(cde.price / 10)
        bal = float(ref_balance * self.refferal)
        return bal

    def total_earnings(self):
        tota = float(self.balance + self.total_ref_ernings())
        return tota


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify( rand_slug() + "-" + self.username)
        super(Account, self).save(*args, **kwargs)

    

