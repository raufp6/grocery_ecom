# Generated by Django 4.2.1 on 2023-07-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0103_alter_cartorder_coupon_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='coupon_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
    ]
