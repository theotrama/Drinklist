# Generated by Django 3.0.3 on 2020-05-16 16:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('drinkcounter', '0008_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
