# Generated by Django 4.2.4 on 2023-08-27 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_otp_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
