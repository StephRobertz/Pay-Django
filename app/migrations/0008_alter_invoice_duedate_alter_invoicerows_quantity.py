# Generated by Django 4.2.4 on 2024-01-23 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_invoice_duedate_alter_invoicerows_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='dueDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 6, 13, 46, 44, 432756)),
        ),
        migrations.AlterField(
            model_name='invoicerows',
            name='quantity',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
