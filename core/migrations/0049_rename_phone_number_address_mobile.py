# Generated by Django 4.2.1 on 2023-07-09 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_remove_cartitem_cart_cartitem_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='phone_number',
            new_name='mobile',
        ),
    ]