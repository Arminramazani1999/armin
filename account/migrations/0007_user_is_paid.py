# Generated by Django 4.2.4 on 2023-09-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
