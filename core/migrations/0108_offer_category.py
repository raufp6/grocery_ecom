# Generated by Django 4.2.1 on 2023-07-29 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
    ]