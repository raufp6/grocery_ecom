# Generated by Django 4.2.1 on 2023-07-07 12:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0037_shoppingcart_shoppingcartitems'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoppingCart',
            new_name='Cart',
        ),
        migrations.RenameModel(
            old_name='ShoppingCartItems',
            new_name='CartItems',
        ),
    ]