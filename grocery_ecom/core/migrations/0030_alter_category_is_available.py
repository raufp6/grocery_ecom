# Generated by Django 4.2.1 on 2023-07-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_remove_category_desc_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]