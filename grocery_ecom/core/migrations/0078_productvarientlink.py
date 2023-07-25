# Generated by Django 4.2.1 on 2023-07-24 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_alter_varientvalue_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVarientLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.product')),
                ('varient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.varient')),
            ],
            options={
                'verbose_name_plural': 'Product Varient Link',
            },
        ),
    ]
