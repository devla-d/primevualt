# Generated by Django 3.1.6 on 2021-03-16 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210316_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]