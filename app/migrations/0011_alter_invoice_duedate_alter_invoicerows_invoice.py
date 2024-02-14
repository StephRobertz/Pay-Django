# Generated by Django 4.2.4 on 2024-02-13 09:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_invoicerows_vat_amount_alter_invoice_duedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='dueDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 27, 11, 17, 27, 652102)),
        ),
        migrations.AlterField(
            model_name='invoicerows',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.invoice'),
        ),
    ]
