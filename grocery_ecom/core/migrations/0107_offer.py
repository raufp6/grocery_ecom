# Generated by Django 4.2.1 on 2023-07-29 04:03

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_remove_whishlist_products_whishlist_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('off_percent', models.PositiveIntegerField()),
                ('start_date', models.DateField(validators=[core.models.validate_expiry_date])),
                ('end_date', models.DateField()),
            ],
        ),
    ]