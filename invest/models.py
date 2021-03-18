from django.db import models
from accounts.models import Account
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.text import slugify
import random
import string



def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))




class Payment(models.Model):
    STATUS = (
        ("PENDING", "PENDING"),
        ("COMPLETED", "COMPLETED"),
    
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    coupon = models.IntegerField()
    status = models.CharField(max_length= 20, choices=STATUS,  blank=True,null=True)

    def __str__(self):
        return f"{self.user.fullname} invested {self.amount}"


class Withdraw(models.Model):
    STATE = (
        ("PENDING", "PENDING"),
        ("COMPLETED", "COMPLETED"),
    
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    status = models.CharField(max_length= 20, choices=STATE,  blank=True,null=True)


    def __str__(self):
        return f"{self.user.fullname} withdraw {self.amount}"



class Post(models.Model):
    CATEGORY = (
        ("Culture", "Culture"),
        ("Entertainment", "Entertainment"),
        ("Education", "Education"),
        ("Gist", "Gist"),
        ("Politics", "Politics"),
        ("Technology", "Technology"),
        ("Sport", "Sport"),
        ("Religion", "Religion"),
        ("Sponsored", "Sponsored"),
    
    )
    title = models.CharField(max_length= 400)
    content = RichTextUploadingField()
    #author = models.ForeignKey(Account, on_delete=models.CASCADE)
    created =  models.DateTimeField(auto_now_add=True)
    category  = models.CharField(max_length=50, choices=CATEGORY)
    slug = models.SlugField()

    class Meta:
            ordering = ('-created',"category")

    def __str__(self):
        return self.title

    def snippet(self):
        return self.content[0:70]


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})



    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(rand_slug() + self.title)
        return super().save(*args, **kwargs)