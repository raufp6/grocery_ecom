# Generated by Django 4.2.1 on 2023-07-25 16:57

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_remove_productvarientconfigeration_product_varient_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=100),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456789', length=5, max_length=10, prefix='sku', unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='productvarientconfigeration',
            name='varient_value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prd_varient_values_label', to='core.varientvalue'),
        ),
        migrations.AlterField(
            model_name='productvarientlink',
            name='varient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prd_varient_item', to='core.varient'),
        ),
    ]
