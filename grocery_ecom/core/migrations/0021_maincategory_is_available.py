# Generated by Django 4.2.1 on 2023-07-03 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_maincategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='maincategory',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]
