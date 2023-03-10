# Generated by Django 3.2.4 on 2022-07-30 07:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setparam', '0011_auto_20220727_2245'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coaljson', '0003_auto_20220730_1426'),
        ('blending', '0018_alter_blendingonunit_tanggal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blendingonunit',
            name='tanggal',
            field=models.DateField(blank=True, default=datetime.date(2022, 7, 30)),
        ),
        migrations.CreateModel(
            name='BlendOnUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(default=datetime.date(2022, 7, 30))),
                ('waktu', models.TimeField()),
                ('persenbio', models.FloatField(default=0)),
                ('persentongkang', models.FloatField(null=True)),
                ('persencoalyard', models.FloatField(null=True)),
                ('kalori', models.FloatField(null=True)),
                ('roh', models.FloatField(null=True)),
                ('coalflow', models.FloatField(null=True)),
                ('ggonet', models.FloatField(null=True)),
                ('biomass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='asbiomass', to='coaljson.coal')),
                ('coalyard', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='incoalyard', to='coaljson.coal')),
                ('tongkang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='intongkang', to='coaljson.coal')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='setparam.unitboiler')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]