# Generated by Django 4.2.1 on 2023-07-07 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_rename_shoppingcart_cart_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItems',
            new_name='CartItem',
        ),
    ]