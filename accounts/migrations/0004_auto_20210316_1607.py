# Generated by Django 3.1.6 on 2021-03-16 15:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210316_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 15, 7, 36, 243321, tzinfo=utc)),
        ),
    ]
