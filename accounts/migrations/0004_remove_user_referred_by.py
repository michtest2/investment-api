# Generated by Django 5.1.5 on 2025-02-15 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_adminpaymentaccounts_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='referred_by',
        ),
    ]
