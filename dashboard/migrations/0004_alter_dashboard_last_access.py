# Generated by Django 5.1.5 on 2025-02-15 05:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_dashboard_options_dashboard_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='last_access',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
