# Generated by Django 4.2.1 on 2023-06-26 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
    ]
