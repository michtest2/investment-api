# Generated by Django 5.1.5 on 2025-02-14 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_adminpaymentaccounts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminpaymentaccounts',
            options={'verbose_name': 'Admin Payment Account', 'verbose_name_plural': 'Admin Payment Accounts'},
        ),
    ]
