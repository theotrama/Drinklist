# Generated by Django 3.0.3 on 2020-09-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinkcounter', '0010_auto_20200913_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beverage',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
