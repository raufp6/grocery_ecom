# Generated by Django 4.2.1 on 2023-07-08 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_rename_cart_id_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='line2',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='type',
            field=models.CharField(blank=True, default='home', max_length=10, null=True),
        ),
    ]