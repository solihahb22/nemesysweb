# Generated by Django 3.2.4 on 2022-07-30 18:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaljson', '0003_auto_20220730_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coalstockunit',
            name='tanggal',
            field=models.DateField(blank=True, default=datetime.date(2022, 7, 31)),
        ),
    ]