# Generated by Django 4.2.4 on 2023-08-31 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_order_is_paid_alter_order_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
