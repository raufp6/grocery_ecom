# Generated by Django 4.2.1 on 2023-06-28 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0006_user_username_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]