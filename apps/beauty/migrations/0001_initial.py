# Generated by Django 2.2.12 on 2020-10-26 10:33

import apps.beauty.models
from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BeautyTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Beauty',
            fields=[
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('beauty_name', models.CharField(max_length=40)),
                ('age', models.IntegerField(null=True)),
                ('birthday', models.DateField(null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('xingzuo', models.CharField(max_length=30, null=True)),
                ('tall', models.CharField(max_length=20, null=True)),
                ('weight', models.CharField(max_length=20, null=True)),
                ('sanwei', models.CharField(max_length=40, null=True)),
                ('job', models.CharField(max_length=30, null=True)),
                ('interested', models.CharField(max_length=100, null=True)),
                ('detail', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('cover_img', models.ImageField(upload_to=apps.beauty.models.create_beauty_folder)),
                ('tags', models.ManyToManyField(related_name='beauty', to='beauty.BeautyTags')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
    ]
