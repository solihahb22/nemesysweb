# Generated by Django 3.2.4 on 2021-09-16 03:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blending', '0006_alter_blendingonunit_tanggal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blendingonunit',
            name='tanggal',
            field=models.DateField(blank=True, default=datetime.date(2021, 9, 16)),
        ),
    ]
