# Generated by Django 4.2.4 on 2023-12-29 12:33

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_invoice_duedate_alter_invoicerows_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='dueDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 12, 14, 33, 20, 14159)),
        ),
        migrations.AlterField(
            model_name='vat',
            name='percent',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.24'), max_digits=5),
        ),
    ]
