# Generated by Django 4.2.1 on 2023-07-26 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0085_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='core.variation'),
        ),
    ]