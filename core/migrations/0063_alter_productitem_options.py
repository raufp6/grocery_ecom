# Generated by Django 4.2.1 on 2023-07-19 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_varient_varientvalue_productitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productitem',
            options={'verbose_name_plural': 'Product Items'},
        ),
    ]