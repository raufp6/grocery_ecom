# Generated by Django 4.2.1 on 2023-07-03 12:33

import django.core.validators
from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_brand_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghi123456789', length=10, max_length=20, prefix='cat', unique=True)),
                ('title', models.CharField(default=None, max_length=100)),
                ('title2', models.CharField(default=None, max_length=100)),
                ('image', models.FileField(default='category-icon.png', upload_to='category', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'webp', 'jpeg', 'svg'])])),
                ('is_featured', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Main Categories',
            },
        ),
    ]
