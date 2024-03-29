# Generated by Django 4.2.4 on 2024-02-01 08:57

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_invoice_duedate_alter_invoicerows_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicerows',
            name='total_with_tax',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='dueDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 10, 57, 22, 539827)),
        ),
    ]
