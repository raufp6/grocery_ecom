# Generated by Django 4.2.1 on 2023-08-08 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0116_alter_variation_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]