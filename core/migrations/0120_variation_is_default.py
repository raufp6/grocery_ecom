# Generated by Django 4.2.1 on 2023-08-09 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0119_variation_mrp_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
