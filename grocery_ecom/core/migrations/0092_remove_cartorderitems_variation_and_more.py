# Generated by Django 4.2.1 on 2023-07-27 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0091_cartorder_is_ordered_cartorderitems_package_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorderitems',
            name='variation',
        ),
        migrations.AddField(
            model_name='cartorderitems',
            name='variations',
            field=models.ManyToManyField(blank=True, to='core.variation'),
        ),
    ]
