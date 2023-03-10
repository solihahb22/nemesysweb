# Generated by Django 3.2.4 on 2021-06-22 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setparam', '0002_alter_parameterboiler_nilaikalorunit'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitBoiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namapltu', models.CharField(max_length=100)),
                ('namaunit', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BoilerSetting',
            fields=[
                ('unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='setparam.unitboiler')),
                ('dayanet', models.JSONField(default=None)),
                ('AH', models.FloatField()),
                ('VM', models.IntegerField()),
                ('nilaikalorunit', models.CharField(max_length=10)),
                ('corner', models.JSONField(default=None)),
            ],
        ),
    ]
