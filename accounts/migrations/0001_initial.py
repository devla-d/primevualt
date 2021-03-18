# Generated by Django 3.1.6 on 2021-03-15 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('fullname', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('country', models.CharField(choices=[('NIGERIA', 'NIGERIA'), ('GHANA', 'GHANA'), ('UGANDA', 'UGANDA'), ('SOUTH AFRICA', 'SOUTH AFRICA'), ('KENYA', 'KENYA')], max_length=30)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(blank=True, default='teamwork.png', null=True, upload_to='profile')),
                ('refferal', models.IntegerField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('investment_amount', models.FloatField(default=0)),
                ('withdraw_amount', models.FloatField(default=0)),
                ('total_earnings', models.FloatField(default=0)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('coupon', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
