# Generated by Django 3.0.3 on 2020-05-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinkcounter', '0006_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='credit',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='Credit',
        ),
    ]
