# Generated by Django 4.2.1 on 2023-07-03 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_category_is_available'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maincategory',
            old_name='title2',
            new_name='desc',
        ),
    ]