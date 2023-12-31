# Generated by Django 4.2.1 on 2023-06-27 19:11

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_user_mobile_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=phone_field.models.PhoneField(max_length=31, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
