# Generated by Django 3.2.4 on 2021-06-19 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='password_time',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='registration_time',
        ),
    ]