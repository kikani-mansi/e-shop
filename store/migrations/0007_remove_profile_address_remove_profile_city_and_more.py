# Generated by Django 5.0.3 on 2024-04-03 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_cart_product_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phonenumber',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
    ]