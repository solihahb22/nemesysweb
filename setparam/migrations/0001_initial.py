# Generated by Django 3.2.4 on 2021-06-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterBoiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namapltu', models.CharField(max_length=100)),
                ('namaunit', models.CharField(max_length=100)),
                ('dayanet', models.JSONField(default=None)),
                ('AH', models.FloatField()),
                ('VM', models.IntegerField()),
                ('nilaikalorunit', models.CharField(max_length=10)),
                ('corner', models.JSONField(default=None)),
            ],
        ),
    ]
