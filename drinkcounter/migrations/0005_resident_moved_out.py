# Generated by Django 3.0.3 on 2020-05-09 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinkcounter', '0004_consumption_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='moved_out',
            field=models.BooleanField(default=False),
        ),
    ]
