# Generated by Django 3.2.4 on 2021-07-11 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('setparam', '0006_parameteroptpembebanan'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlendingOnUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targetkalor', models.IntegerField()),
                ('persenbiomass', models.FloatField()),
                ('coal1', models.TextField(blank=True)),
                ('coal2', models.TextField(blank=True)),
                ('biomass', models.FloatField(default=1)),
                ('cofiring', models.TextField(blank=True)),
                ('settingunit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setparam.parameterblending')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setparam.unitboiler')),
            ],
        ),
    ]
