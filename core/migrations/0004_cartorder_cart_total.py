# Generated by Django 4.2.1 on 2023-08-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_orderaddress_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='cart_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100, null=True),
        ),
    ]
