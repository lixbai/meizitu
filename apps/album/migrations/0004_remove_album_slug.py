# Generated by Django 2.2.12 on 2021-03-25 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20210325_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='slug',
        ),
    ]